from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from . import models
from . import forms
from . import filters
from . import consts


class Log(TemplateView):
    template_name = None    # must be specified by
    model = models.Log
    form_class = forms.Log
    filter_class = filters.Log
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs = self.get_queryset()
        context['page'] = self._get_page(qs)
        context['object_list'] = qs

        context['LOG_LEVEL_CRITICAL'] = consts.LOG_LEVEL_CRITICAL
        context['LOG_LEVEL_ERROR'] = consts.LOG_LEVEL_ERROR
        context['LOG_LEVEL_WARNING'] = consts.LOG_LEVEL_WARNING
        context['LOG_LEVEL_INFO'] = consts.LOG_LEVEL_INFO
        context['LOG_LEVEL_DEBUG'] = consts.LOG_LEVEL_DEBUG
        context['LOG_LEVEL_NOTSET'] = consts.LOG_LEVEL_NOTSET

        form = self.get_form()
        form.is_valid()
        context['form'] = form

        return context

    def get_form(self):
        return self.form_class(self.request.GET or None)

    def get_queryset(self):
        form = self.get_form()
        if form.is_valid():
            params = form.cleaned_data
            qs = self.model.objects.all()
            qs = self.filter_class(params, qs).qs
            return qs
        else:
            return self.model.objects.none()

    def _get_page(self, qs):
        paginator = Paginator(qs, self.paginate_by)

        page_num = self.request.GET.get('page')
        try:
            page = paginator.page(page_num)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        return page

