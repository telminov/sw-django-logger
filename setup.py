# coding: utf-8
# python -m pip install certifi
# export SSL_CERT_FILE=$(python -m certifi)
# python setup.py sdist
# twine upload dist/*
from setuptools import setup, find_packages

setup(
    name='sw-django-logger',
    version='0.0.19',
    description='Log handling and representing for django projects',
    author='Telminov Sergey',
    author_email='sergey@telminov.ru',
    url='https://github.com/telminov/sw-django-logger',
    include_package_data=True,
    packages=find_packages(),
    license='The MIT License',
    test_suite='runtests.runtests',
    install_requires=[
        'django', 'django-filter',
    ],
)
