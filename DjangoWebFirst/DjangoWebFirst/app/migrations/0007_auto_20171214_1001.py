# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-14 02:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20171214_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sys_user',
            name='PassWord',
            field=models.CharField(max_length=128, verbose_name='密码'),
        ),
    ]
