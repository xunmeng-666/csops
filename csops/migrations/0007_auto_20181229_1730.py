# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-29 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csops', '0006_auto_20181229_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='resolve_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='最终解决时间'),
        ),
    ]