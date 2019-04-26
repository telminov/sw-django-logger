# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-10 11:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sw_logger', '0004_auto_20180810_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='level',
            field=models.CharField(max_length=10, choices=[('', ''), ('CRITICAL', 'CRITICAL'), ('ERROR', 'ERROR'), ('WARNING', 'WARNING'), ('INFO', 'INFO'), ('DEBUG', 'DEBUG'), ('NOTSET', 'NOTSET')], default='NOTSET', db_index=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
