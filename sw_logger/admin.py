from django.contrib import admin
from django.utils.html import format_html

from . import consts
from . import models


class InputFilter(admin.SimpleListFilter):
    template = "admin/input_filter.html"

    def lookups(self, request, model_admin):
        return ((),)

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        all_choice["query_parts"] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class LogUsernameFilter(InputFilter):
    parameter_name = 'username'
    title = 'username'

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(username__icontains=self.value())


class LogObjectIDFilter(InputFilter):
    parameter_name = 'object_id'
    title = 'ID объекта'

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(object_id=self.value())


class LogMessageFilter(InputFilter):
    parameter_name = 'message'
    title = 'Сообщение'

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(message__icontains=self.value())


class Log(admin.ModelAdmin):
    list_display = ('get_message', 'get_action', 'get_obj', 'get_changes', 'get_time', 'get_username', 'get_level')
    list_filter = (LogUsernameFilter, LogObjectIDFilter, LogMessageFilter, 'action', 'level', 'created', 'object_name')
    ordering = ('-created', )

    def get_message(self, obj: models.Log):
        return obj.message
    get_message.short_description = 'Сообщение'

    def get_action(self, obj: models.Log):
        actions_rus = {
            consts.ACTION_DELETED: 'Удаление',
            consts.ACTION_UPDATED: 'Обновление',
            consts.ACTION_CREATED: 'Создание',
            consts.ACTION_OTHER: 'Другое',
        }
        action_rus = actions_rus.get(obj.action, '')
        levels_colors = {
            consts.ACTION_DELETED: '#f8d7da',
            consts.ACTION_UPDATED: '#fff3cd',
            consts.ACTION_CREATED: '#d1ecf1',
        }
        level_color = levels_colors.get(obj.action, '#e2e3e5')
        css = f'display:flex; align-items:center; justify-content:center; background-color:{level_color};'
        text_html = f'<div style="{css}">{action_rus}</div>'
        return format_html(text_html)
    get_action.short_description = 'Действие'

    def get_obj(self, obj: models.Log):
        model_name = obj.get_object_model_name()
        model_object = obj.get_model_object()
        if model_name and model_object:
            text = f'{model_name} (id: {model_object.id})'
        else:
            text = ''
        return text
    get_obj.short_description = 'Объект'

    def get_changes(self, obj: models.Log):
        text_html = '<ul>'
        changes = obj.get_changes()
        if changes:
            for field, value in changes.items():
                value = value or ''
                text_html += f'<li><b>{field}</b>: {value}</li>'
        text_html += '</ul>'
        return format_html(text_html)
    get_changes.short_description = 'Изменения'

    def get_time(self, obj: models.Log):
        return obj.created
    get_time.short_description = 'Время'

    def get_username(self, obj: models.Log):
        return obj.username
    get_username.short_description = 'Пользователь'


    def get_level(self, obj: models.Log):
        levels_colors = {
            consts.LOG_LEVEL_CRITICAL: '#dc3545',
            consts.LOG_LEVEL_ERROR: '#dc3545',
            consts.LOG_LEVEL_WARNING: '#ffc107',
            consts.LOG_LEVEL_INFO: '#17a2b8',
        }
        level_color = levels_colors.get(obj.level, '#6c757d')
        css = f'display:flex; align-items:center; justify-content:center; background-color:{level_color}; color: white;'
        text_html = f'<div style="{css}">{obj.level}</div>'
        return format_html(text_html)
    get_level.short_description = 'Уровень'
