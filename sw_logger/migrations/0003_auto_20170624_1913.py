# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-24 19:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sw_logger', '0002_auto_20170624_1618'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='dc',
            new_name='created',
        ),
    ]
