# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('taskname', models.CharField(max_length=255, verbose_name=b'\xe4\xbd\x9c\xe4\xb8\x9a\xe5\x90\x8d\xe7\xa7\xb0')),
                ('qtime', models.DateField(verbose_name=b'\xe6\x9c\x80\xe6\x99\x9a\xe6\x8f\x90\xe4\xba\xa4\xe6\x97\xb6\xe9\x97\xb4')),
                ('files', models.TextField(verbose_name=b'\xe9\x99\x84\xe4\xbb\xb6')),
                ('desc', models.TextField(null=True, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('course', models.ForeignKey(verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b', to='info.ClassCourseInfo')),
            ],
            options={
                'verbose_name': '\u8bfe\u7a0b\u4f5c\u4e1a',
                'verbose_name_plural': '\u8bfe\u7a0b\u4f5c\u4e1a',
            },
        ),
        migrations.CreateModel(
            name='TaskRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('score', models.IntegerField(verbose_name=b'\xe6\x88\x90\xe7\xbb\xa9')),
                ('feedback', models.TextField(null=True, verbose_name=b'\xe5\x8f\x8d\xe9\xa6\x88', blank=True)),
                ('task', models.ForeignKey(verbose_name=b'\xe4\xbd\x9c\xe4\xb8\x9a', to='student.Task')),
                ('user', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to='base.User')),
            ],
            options={
                'verbose_name': '\u4f5c\u4e1a\u8bb0\u5f55',
                'verbose_name_plural': '\u4f5c\u4e1a\u8bb0\u5f55',
            },
        ),
    ]
