# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-18 14:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csops', '0002_job_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagepath', models.CharField(blank=True, max_length=128, null=True, verbose_name='路径')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='csops.Job', verbose_name='工单')),
            ],
            options={
                'verbose_name': '图片',
                'verbose_name_plural': '图片',
            },
        ),
    ]
