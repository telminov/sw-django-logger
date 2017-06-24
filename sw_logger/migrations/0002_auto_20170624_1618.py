# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-24 16:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sw_logger', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='http_general',
        ),
        migrations.AddField(
            model_name='log',
            name='http_method',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='log',
            name='http_path',
            field=models.TextField(blank=True),
        ),
    ]
