from typing import Type
import json
from logging import Handler, LogRecord
from django.http import QueryDict
from django.db.models import Model
from django.conf import settings


class DbHandler(Handler):
    @staticmethod
    def get_log_model() -> Type[Model]:
        from . import models
        return models.Log

    def emit(self, record: LogRecord):
        # internal import for prevent circular import
        from . import tools

        func_name = '%s.%s; line %s' % (record.module, record.funcName, record.lineno)

        log = self.get_log_model()(
            message=record.msg,
            func_name=func_name,
            level=record.levelname,
        )

        self._process_request_data(log, record)

        if hasattr(record, 'object'):
            log.object_id = record.object.id
            log.object_name = record.object.LOG_NAME
            log.object_data = json.dumps(tools.model_to_dict(record.object))

        if hasattr(record, 'object_name'):
            log.object_name = record.object_name

        if hasattr(record, 'object_id'):
            log.object_id = record.object_id

        if hasattr(record, 'action'):
            log.action = record.action

        if hasattr(record, 'extra'):
            log.extra = json.dumps(record.extra)

        self._emit_extra(log, record)

        log.save()

    def _emit_extra(self, log, record: LogRecord):
        """
            Extension point. For example, for processing additional fields.
        """
        pass

    @classmethod
    def _process_request_data(cls, log, record: LogRecord) -> None:
        if not hasattr(record, 'request') or not record.request:
            return

        request = record.request

        log.http_method = request.method
        log.http_path = request.path

        if getattr(settings, 'SW_LOGGER_LOG_REQUEST_PARAMS', False):
            log.http_request_get = json.dumps(cls._query_to_dict(request.GET))
            if isinstance(request.POST, QueryDict):
                log.http_request_post = json.dumps(cls._query_to_dict(request.POST))

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            log.http_referrer = x_forwarded_for.split(',')[-1].strip()
        else:
            log.http_referrer = request.META.get('REMOTE_ADDR')

        if getattr(request, 'user', None):
            log.user_id = getattr(request.user, 'id', None)
            log.username = getattr(request.user, 'username', None)

    @classmethod
    def _query_to_dict(cls, params: QueryDict) -> dict:
        result = {}
        for key in params:
            values = params.getlist(key)
            if len(values) > 1:
                result[key] = values
            else:
                result[key] = params[key]
        return result
