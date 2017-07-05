# sw-django-logger
Log handling and representing for django projects

[![Build Status](https://travis-ci.org/telminov/sw-django-logger.svg?branch=master)](https://travis-ci.org/telminov/sw-django-logger)

## Installation
```
pip install sw-django-logger
```

Add to settings.py
```python
INSTALLED_APPS = [
  ...
  'sw_logger',
  ...
]
...
LOGGING = {
    ...
    'handlers': {
        ...
        'db': {
            'level': 'INFO',
            'class': 'sw_logger.handlers.DbHandler',
        },
    },
    'loggers': {
        ...
        'db': {
            'handlers': ['db'],
            'level': 'INFO',
        }
    }
}
```
Migrate
```
./manage.py migrate
```

## Logging
Add unique for project LOG_NAME attribute to models
```python
class Book(models.Model)
    LOG_NAME = 'book'
    name = ...
```

Using in view:
```python
import logging
logger = logging.getLogger('db')

class Update(UpdateView):
    ...
    def form_valid(self, form):
        response = super().form_valid(form)
       
        logger.info(
            'Some message',
            extra={
                'action': sw_logger.consts.ACTION_UPDATED,
                'request': self.request,
                'object': self.get_object(),
            }
        )
        return response
```

## Viewing log
Create log view
```python
class Log(sw_logger.views.Log):
    template_name = 'core/report/log.html'

```

Add to urls.py
```python
...
urlpatterns = [
...
    url(r'^log/$', core.views.Log.as_view(), name='log'),
...
]
```

Add template
```
...
{{ form }}

<table>
    <thead>
        <tr>
            <th>#</th>
            <th>Message</th>
            <th>Object</th>
            <th>Changes</th>
            <th>Time</th>
            <th>User</th>
            <th>Level</th>
        </tr>
    </thead>

    <tbody>
    {% for object in page.object_list %}
        <tr {% if object.action == 'created' %}class="info"
            {% elif object.action == 'deleted' %}class="error"
            {% elif object.action == 'updated' %}class="warning"
            {% endif %}>

            <td>{{ forloop.counter0|add:page.start_index }}</td>
            <td>{{ object.message }}</td>
            <td>{{ object.get_object_model_name }}</td>
            <td>
                <ul>
                    {% for field, value in object.get_changes.items %}
                        <li><b>{{ field }}</b>: {{ value|default:'' }}</li>
                    {% endfor %}
                </ul>
            </td>
            <td>{{ object.get_user }}</td>
            <td>
                <span class="badge
                    {% if object.level == object.LOG_LEVEL_CRITICAL or object.level == object.LOG_LEVEL_ERROR %}badge-danger
                    {% elif object.level == object.LOG_LEVEL_WARNING %}badge-warning
                    {% elif object.level == object.LOG_LEVEL_INFO %}badge-info
                    {% endif %}
                  "
                >
                    {{ object.get_level_display }}
                </span>
            </td>
        </tr>
    {% endfor %}
    </tbody>
```