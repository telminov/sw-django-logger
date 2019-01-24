import django.forms
import datetime
import decimal

from collections import OrderedDict
from typing import List, Type, Optional
from django.db.models import Model, ForeignKey, UUIDField, ManyToManyField
from django.db.models.fields.files import FieldFile
from django.db.models.query import ValuesListIterable, QuerySet
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


def get_models_choices() -> List:
    choices = []
    for model in get_models():
        choices.append((model.LOG_NAME, model._meta.verbose_name))
    return choices


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


def object_display_from_log(log: models.Log) -> Optional[dict]:
    """
    :param log:
    :return: human oriented object data representation (use verbose names and etc)
    """
    if not log.object_data:
        return

    display_data = OrderedDict()
    object_data = log.get_object_data()
    model = get_model_by_log_name(log.object_name)

    for field in model._meta.fields:
        value = object_data.get(field.name)

        if isinstance(field, ForeignKey):
            filter_params = {}
            field_rel = field.rel if hasattr(field, 'rel') else field.remote_field
            filter_params[field_rel.field_name] = value
            if hasattr(field_rel, 'to'):
                related_qs = field_rel.to.objects.filter(**filter_params)
            else:
                related_qs = field_rel.field.related_model.objects.filter(**filter_params)
            if len(related_qs):
                value = related_qs[0]

        if isinstance(value, list):
            value = ', '.join(value)

        display_data[field.verbose_name] = value

    for field in model._meta.many_to_many:
        value = object_data.get(field.name, [])
        related_qs = field.related_model.objects.filter(pk__in=value)
        display_data[field.verbose_name] = ', '.join(sorted([str(i) for i in related_qs]))

    return display_data


def get_changes_display(previous_log: models.Log, current_log: models.Log) -> Optional[dict]:
    """
    :param previous_log:
    :param current_log:
    :return: human oriented representation of differences between objects data two of log records
    """
    previous_display = previous_log.get_object_data_display()
    current_display = current_log.get_object_data_display()

    if not previous_display or not current_display:
        return

    changes_display = OrderedDict()
    for field_name in current_display.keys():
        if current_display[field_name] != previous_display.get(field_name):
            changes_display[field_name] = current_display[field_name]

    return changes_display


def model_to_dict(obj: Model) -> dict:
    obj_dict = django.forms.model_to_dict(obj)
    obj_dict = _converter(obj_dict)

    # model_to_dict from django.forms skip some fields... Add it.
    for field in obj._meta.fields:
        if isinstance(field, UUIDField):
            obj_dict[field.name] = str(getattr(obj, field.name))

    # replace m2m object instance by pk
    for field_name, value in obj_dict.items():
        if isinstance(value, list):
            new_value = []
            for item in value:
                if isinstance(item, Model):
                    new_value.append(item.pk)
                else:
                    new_value.append(item)
            obj_dict[field_name] = new_value

    return obj_dict


def _converter(obj_dict: dict) -> dict:
    for key, value in obj_dict.items():
        if isinstance(value, dict):
            obj_dict[key] = _converter(value)

        elif isinstance(value, FieldFile):
            obj_dict[key] = str(value)

        elif isinstance(value, datetime.date):
            obj_dict[key] = value.isoformat()

        elif isinstance(value, datetime.time):
            obj_dict[key] = value.isoformat()

        elif isinstance(value, datetime.datetime):
            obj_dict[key] = value.isoformat(sep=' ')

        elif isinstance(value, ValuesListIterable):
            obj_dict[key] = list(value)

        elif isinstance(value, QuerySet):
            obj_dict[key] = list(value.values_list('pk', flat=True))

        elif isinstance(value, bytes):
            obj_dict[key] = value.decode('utf-8')

        elif isinstance(value, decimal.Decimal):
            obj_dict[key] = [str(i) for i in [value]]

    return obj_dict
