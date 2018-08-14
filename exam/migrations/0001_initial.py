# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20180330_1330'),
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('examname', models.CharField(max_length=255, verbose_name=b'\xe8\x80\x83\xe8\xaf\x95\xe5\x90\x8d\xe7\xa7\xb0')),
                ('score', models.CharField(max_length=20, verbose_name=b'\xe5\x88\x86\xe6\x95\xb0')),
                ('subjectclassranking', models.CharField(max_length=20, null=True, verbose_name=b'\xe7\xa7\x91\xe7\x9b\xae\xe7\x8f\xad\xe7\xba\xa7\xe6\x8e\x92\xe5\x90\x8d', blank=True)),
                ('classranking', models.CharField(max_length=20, null=True, verbose_name=b'\xe7\xbb\xbc\xe5\x90\x88\xe7\x8f\xad\xe7\xba\xa7\xe6\x8e\x92\xe5\x90\x8d', blank=True)),
                ('subjectgraderanking', models.CharField(max_length=20, null=True, verbose_name=b'\xe7\xa7\x91\xe7\x9b\xae\xe5\xb9\xb4\xe7\xba\xa7\xe6\x8e\x92\xe5\x90\x8d', blank=True)),
                ('graderanking', models.CharField(max_length=20, null=True, verbose_name=b'\xe7\xbb\xbc\xe5\x90\x88\xe5\xb9\xb4\xe7\xba\xa7\xe6\x8e\x92\xe5\x90\x8d', blank=True)),
                ('analysis', models.TextField(null=True, verbose_name=b'\xe5\x88\x86\xe6\x9e\x90', blank=True)),
                ('examsubject', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe8\x80\x83\xe8\xaf\x95\xe7\xa7\x91\xe7\x9b\xae', blank=True, to='info.CourseInfo', null=True)),
                ('user', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to='base.User')),
            ],
            options={
                'verbose_name': '\u6210\u7ee9\u8bb0\u5f55',
                'verbose_name_plural': '\u6210\u7ee9\u8bb0\u5f55',
            },
        ),
    ]
