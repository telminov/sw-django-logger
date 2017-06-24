from django import forms
from . import consts
from . import tools


class Log(forms.Form):
    ACTION_CHOICES = [('', '')] + list(consts.ACTION_CHOICES)
    LOG_LEVEL_CHOICES = [('', '')] + list(consts.LOG_LEVEL_CHOICES)

    datetime_from = forms.DateTimeField()
    datetime_to = forms.DateTimeField()

    action = forms.MultipleChoiceField(required=False, choices=consts.ACTION_CHOICES)
    level = forms.MultipleChoiceField(required=False, choices=consts.LOG_LEVEL_CHOICES)
    object_name = forms.MultipleChoiceField(required=False, choices=tools.get_models_choices())
    message = forms.CharField(required=False)
    username = forms.CharField(required=False)
