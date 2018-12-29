# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-29 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='名称')),
            ],
            options={
                'verbose_name': '问题分类',
                'verbose_name_plural': '问题分类',
            },
        ),
    ]
