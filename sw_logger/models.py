import json
import pprint
from typing import Optional
from django.db import models
from django.contrib.auth import get_user_model
from . import consts


class Log(models.Model):
    ACTION_CHOICES = [('', '')] + list(consts.ACTION_CHOICES)
    LOG_LEVEL_CHOICES = [('', '')] + list(consts.LOG_LEVEL_CHOICES)

    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default='')
    message = models.CharField(max_length=255)
    func_name = models.CharField(max_length=255)
    level = models.CharField(max_length=10, choices=LOG_LEVEL_CHOICES, default='NOTSET', db_index=True)

    http_path = models.TextField(blank=True)
    http_method = models.TextField(blank=True)
    http_request_get = models.TextField(blank=True)
    http_request_post = models.TextField(blank=True)
    http_referrer = models.CharField(max_length=255, blank=True)

    user_id = models.IntegerField(db_index=True, null=True)
    username = models.CharField(max_length=255, db_index=True, blank=True)

    object_name = models.CharField(max_length=255, db_index=True, blank=True)
    object_id = models.IntegerField(db_index=True, null=True)
    fk_object_id = models.IntegerField(db_index=True, null=True)
    object_data = models.TextField(blank=True)

    extra = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('id', )

    def get_model_object(self) -> models.Model:
        from . import tools

        if not hasattr(self, '_got_model_object'):
            self._got_model_object = tools.object_from_log(self)

        return self._got_model_object

    def get_object_model_name(self) -> Optional[str]:
        model_object = self.get_model_object()
        if not model_object:
            return

        name = model_object._meta.verbose_name
        return name

    def get_object_data(self) -> Optional[dict]:
        if not self.object_data:
            return

        return json.loads(self.object_data)

    def get_object_data_display(self) -> Optional[dict]:
        from . import tools
        return tools.object_display_from_log(self)

    def get_user(self):
        if not self.user_id:
            return

        User = get_user_model()
        return User.objects.get(id=self.user_id)

    def get_previous_object_log(self) -> Optional['Log']:
        """
        :return: previous log record for same object (same object_name and object_id)
        """
        if not self.object_data:
            return

        previous_qs = Log.objects.filter(
            id__lt=self.id,
            object_name=self.object_name,
            object_id=self.object_id,
        )
        if previous_qs:
            return previous_qs.last()

    def get_changes(self) -> Optional[dict]:
        from . import tools

        previous_object_log = self.get_previous_object_log()
        if not previous_object_log:
            return self.get_object_data_display()

        return tools.get_changes_display(previous_object_log, self)

    def get_extra_data(self):
        """
        try parse json from extra-field
        """
        if not self.extra:
            return

        try:
            return json.loads(self.extra)
        except Exception:
            pass

    def get_extra_pretty(self):
        """
        pretty output extra-field data
        """
        extra_data = self.get_extra_data()
        if not extra_data:
            return

        return pprint.pformat(extra_data)

    def get_http_request_get_pretty(self):
        """
        pretty output extra-field data
        """
        if not self.http_request_get:
            return

        request_data = json.loads(self.http_request_get)
        if not request_data:
            return

        return pprint.pformat(request_data)

    def get_http_request_post_pretty(self):
        """
        pretty output extra-field data
        """
        if not self.http_request_post:
            return

        request_data = json.loads(self.http_request_post)
        if not request_data:
            return

        return pprint.pformat(request_data)
