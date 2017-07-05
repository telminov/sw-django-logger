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

## Logging
