from typing import List, Type, Optional

from django.db.models import Model, ForeignKey
from django.apps import apps
from . import LoggerException
from . import models


def get_models() -> List[Type[Model]]:
    """
    :return: models under logging (have LOG_NAME attribute)
    """
    models = []

    for model in apps.get_models():
        if hasattr(model, 'LOG_NAME') and model.LOG_NAME:
            models.append(model)

    return models


def get_model_by_log_name(log_name) -> Type[Model]:
    for item in get_models():
        if item.LOG_NAME == log_name:
            return item
    raise LoggerException('Model with LOG_NAME "%s" not found' % log_name)


def object_from_log(log: models.Log) -> Optional[Model]:
    """
        create model object in memory from log data
    """
    object_data = log.get_object_data()

    if not object_data:
        return

    model = get_model_by_log_name(log.object_name)

    fields = {}
    for field in model._meta.fields:
        fields[field.name] = field

    model_object = model()

    # first - "id", for many-to-many recreation
    if 'id' in fields:
        model_object.id = object_data['id']

    # other fields
    for field_name, value in object_data.items():
        # skip other model fields (for example, ManyToMany)
        if field_name not in fields:
            continue

        # check is field FK
        if isinstance(fields.get(field_name), ForeignKey):
            # for FK fields add "_id" to field name
            field_name += '_id'

        setattr(model_object, field_name, value)

    return model_object
