# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-27 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csops', '0006_auto_20181227_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='timeout',
            field=models.BooleanField(verbose_name='超时'),
        ),
    ]