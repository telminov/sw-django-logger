import json
from typing import Optional
from django.db import models
from django.contrib.auth.models import User
from . import consts


class Log(models.Model):
    ACTION_CHOICES = [('', '')] + list(consts.ACTION_CHOICES)
    LOG_LEVEL_CHOICES = [('', '')] + list(consts.LOG_LEVEL_CHOICES)

    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default='')
    message = models.CharField(max_length=255)
    func_name = models.CharField(max_length=255)
    level = models.CharField(max_length=10, choices=LOG_LEVEL_CHOICES, default='NOTSET')

    http_path = models.TextField(blank=True)
    http_method = models.TextField(blank=True)
    http_request_get = models.TextField(blank=True)
    http_request_post = models.TextField(blank=True)
    http_referrer = models.CharField(max_length=255, blank=True)

    user_id = models.IntegerField(db_index=True, null=True)
    username = models.CharField(max_length=255, db_index=True, blank=True)

    object_name = models.CharField(max_length=255, db_index=True, blank=True)
    object_id = models.IntegerField(db_index=True, null=True)
    object_data = models.TextField(blank=True)

    extra = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_model_object(self) -> models.Model:
        from . import tools

        if not hasattr(self, '_got_model_object'):
            self._got_model_object = tools.object_from_log(self)

        return self._got_model_object

    def get_object_model_name(self) -> str:
        model_object = self.get_model_object()
        if not model_object:
            return

        name = model_object._meta.verbose_name
        return name

    def get_object_data(self) -> Optional[dict]:
        if not self.object_data:
            return

        return json.loads(self.object_data)

    def get_user(self):
        if not self.user_id:
            return

        return User.objects.get(id=self.user_id)