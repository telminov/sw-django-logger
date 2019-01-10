import django_filters
from . import models


class Log(django_filters.FilterSet):
    datetime_from = django_filters.DateTimeFilter('created', lookup_expr='gte')
    datetime_to = django_filters.DateTimeFilter('created', lookup_expr='lte')
    message = django_filters.CharFilter('message', lookup_expr='icontains')
    action = django_filters.MultipleChoiceFilter('action', choices=models.Log.ACTION_CHOICES)
    level = django_filters.MultipleChoiceFilter('level', choices=models.Log.LOG_LEVEL_CHOICES)

    class Meta:
        model = models.Log
        fields = ['datetime_from', 'datetime_to', 'action', 'level', 'object_name', 'message', 'username',]
