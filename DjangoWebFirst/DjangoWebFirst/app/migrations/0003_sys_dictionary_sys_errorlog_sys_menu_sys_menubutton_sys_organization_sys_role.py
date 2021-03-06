# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-13 04:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20171213_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sys_Dictionary',
            fields=[
                ('KeyId', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('ParentId', models.CharField(max_length=50, verbose_name='父级')),
                ('FullName', models.CharField(max_length=50, verbose_name='称呼')),
                ('Img', models.CharField(max_length=50, verbose_name='图片')),
                ('Url', models.CharField(max_length=50, verbose_name='链接')),
                ('Description', models.CharField(max_length=50, verbose_name='描述')),
                ('SortNum', models.IntegerField(verbose_name='排序')),
                ('IsDeleted', models.BooleanField(verbose_name='是否删除')),
                ('DateTime', models.DateTimeField(verbose_name='时间')),
                ('PIds', models.CharField(max_length=50, verbose_name='所有父级')),
            ],
        ),
        migrations.CreateModel(
            name='Sys_ErrorLog',
            fields=[
                ('KeyId', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('Title', models.CharField(max_length=50, verbose_name='标题')),
                ('ErrorMsg', models.CharField(max_length=50, verbose_name='错误详情')),
                ('DateTime', models.DateTimeField(verbose_name='时间')),
            ],
        ),
        migrations.CreateModel(
            name='Sys_Menu',
            fields=[
                ('KeyId', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('ParentId', models.CharField(max_length=50, verbose_name='父级')),
                ('FullName', models.CharField(max_length=50, verbose_name='称呼')),
                ('Icon', models.CharField(max_length=50, verbose_name='图标')),
                ('NavigateUrl', models.CharField(max_length=50, verbose_name='菜单链接')),
                ('IsRoot', models.BooleanField(verbose_name='是否为根菜单')),
                ('Description', models.CharField(max_length=50, verbose_name='描述')),
                ('SortNum', models.IntegerField(verbose_name='排序')),
                ('IsDeleted', models.BooleanField(verbose_name='是否删除')),
                ('DateTime', models.DateTimeField(verbose_name='时间')),
            ],
        ),
        migrations.CreateModel(
            name='Sys_MenuButton',
            fields=[
                ('KeyId', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('MenuId', models.CharField(max_length=50, verbose_name='菜单ID')),
                ('ButtonId', models.CharField(max_length=50, verbose_name='按钮ID')),
                ('DateTime', models.DateTimeField(verbose_name='时间')),
            ],
        ),
        migrations.CreateModel(
            name='Sys_Organization',
            fields=[
                ('KeyId', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('ParentId', models.CharField(max_length=50, verbose_name='父级ID')),
                ('FullName', models.CharField(max_length=50, verbose_name='名称')),
                ('Phone', models.CharField(max_length=50, verbose_name='组织联系电话')),
                ('Description', models.CharField(max_length=50, verbose_name='地址')),
                ('SortNum', models.IntegerField(verbose_name='排序')),
                ('IsDeleted', models.BooleanField(verbose_name='是否删除')),
                ('DateTime', models.DateTimeField(verbose_name='时间')),
                ('PIds', models.CharField(max_length=50, verbose_name='所有父级ID')),
            ],
        ),
        migrations.CreateModel(
            name='Sys_Role',
            fields=[
                ('KeyId', models.AutoField(primary_key=True, serialize=False, verbose_name='主键ID')),
                ('FullName', models.CharField(max_length=50, verbose_name='名称')),
                ('Description', models.CharField(max_length=50, verbose_name='描述')),
                ('IsDeleted', models.BooleanField(verbose_name='是否删除')),
                ('DateTime', models.DateTimeField(verbose_name='时间')),
            ],
        ),
    ]
