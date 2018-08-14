# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('action', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\x8a\xa8\xe4\xbd\x9c', blank=True)),
                ('content', models.TextField(null=True, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9', blank=True)),
                ('model', models.CharField(max_length=64, null=True, verbose_name=b'\xe6\xa8\xa1\xe5\x9e\x8b', blank=True)),
                ('objsid', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xaf\xb9\xe8\xb1\xa1IDs', blank=True)),
                ('model_cn', models.CharField(max_length=255, null=True, verbose_name=b'\xe4\xb8\xad\xe6\x96\x87\xe4\xbb\xb6\xe6\xa8\xa1\xe5\x9e\x8b\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
            ],
            options={
                'verbose_name': '\u65e5\u5fd7',
                'verbose_name_plural': '\u65e5\u5fd7',
            },
        ),
        migrations.CreateModel(
            name='KeyValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('key', models.CharField(unique=True, max_length=255, verbose_name=b'\xe5\x81\xa5', db_index=True)),
                ('type', models.CharField(default=b'text', max_length=255, null=True, verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b', blank=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('value', models.TextField(max_length=65535, null=True, verbose_name=b'\xe5\x80\xbc', blank=True)),
                ('other', models.CharField(max_length=255, null=True, verbose_name=b'\xe9\x99\x84\xe5\x8a\xa0', blank=True)),
            ],
            options={
                'ordering': ['ordering'],
                'verbose_name': '\u8bbe\u7f6e',
                'verbose_name_plural': '\u8bbe\u7f6e',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('name', models.CharField(max_length=255, verbose_name=b'\xe8\xa7\x92\xe8\x89\xb2\xe5\x90\x8d\xe7\xa7\xb0')),
                ('role', models.CharField(max_length=255, verbose_name=b'\xe8\xa7\x92\xe8\x89\xb2\xe6\x9d\x83\xe9\x99\x90')),
                ('oprations', models.TextField(verbose_name=b'\xe6\x93\x8d\xe4\xbd\x9c')),
                ('model_permission', models.TextField(null=True, verbose_name=b'\xe6\xa8\xa1\xe5\x9e\x8b\xe6\x9d\x83\xe9\x99\x90', blank=True)),
            ],
            options={
                'verbose_name': '\u89d2\u8272',
                'verbose_name_plural': '\u89d2\u8272',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('username', models.CharField(unique=True, max_length=32, verbose_name=b'\xe7\x99\xbb\xe5\xbd\x95\xe5\xb8\x90\xe5\x8f\xb7', db_index=True)),
                ('password', models.CharField(max_length=32, verbose_name=b'\xe5\x8a\xa0\xe5\xaf\x86\xe5\xaf\x86\xe7\xa0\x81')),
                ('truename', models.CharField(db_index=True, max_length=128, null=True, verbose_name=b'\xe7\x9c\x9f\xe5\xae\x9e\xe5\xa7\x93\xe5\x90\x8d', blank=True)),
                ('nickname', models.CharField(max_length=255, verbose_name=b'\xe6\x98\xb5\xe7\xa7\xb0', db_index=True)),
                ('email', models.EmailField(db_index=True, max_length=254, null=True, verbose_name=b'\xe7\x94\xb5\xe5\xad\x90\xe9\x82\xae\xe4\xbb\xb6', blank=True)),
                ('phone', models.CharField(db_index=True, max_length=64, null=True, verbose_name=b'\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe7\xa0\x81', blank=True)),
                ('homephone', models.CharField(db_index=True, max_length=64, null=True, verbose_name=b'\xe5\xae\xb6\xe5\xba\xad\xe7\x94\xb5\xe8\xaf\x9d', blank=True)),
                ('icon', models.CharField(max_length=255, null=True, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\xa4\xb4\xe5\x83\x8f', blank=True)),
                ('userinfo', models.TextField(null=True, verbose_name=b'\xe4\xb8\xaa\xe4\xba\xba\xe7\xae\x80\xe4\xbb\x8b', blank=True)),
                ('status', models.IntegerField(default=0, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', editable=False, choices=[(0, b'\xe6\xad\xa3\xe5\xb8\xb8'), (-1, b'\xe5\xb7\xb2\xe9\x94\x81\xe5\xae\x9a')])),
                ('salt', models.CharField(default=b'inruan.com', max_length=32, verbose_name=b'\xe5\xaf\x86\xe7\xa0\x81\xe7\x9b\x90\xe5\xb7\xb4', blank=True)),
                ('token', models.CharField(db_index=True, max_length=128, null=True, verbose_name=b'\xe8\xae\xbf\xe9\x97\xae\xe4\xbb\xa4\xe7\x89\x8c', blank=True)),
                ('rolelist', models.TextField(default=[], verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe6\x9d\x83\xe9\x99\x90', editable=False)),
            ],
            options={
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237',
            },
        ),
    ]
