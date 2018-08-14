# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe5\xb9\xb4\xe7\xba\xa7\xe6\x88\x96\xe5\xb1\x8a\xe6\xac\xa1', blank=True, to='info.GradeInfo', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe8\xa7\x92\xe8\x89\xb2', blank=True, to='base.Role', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe5\xad\xa6\xe6\xa0\xa1', blank=True, to='info.SchoolInfo', null=True),
        ),
        migrations.AddField(
            model_name='actionlog',
            name='user',
            field=models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', blank=True, to='base.User', null=True),
        ),
    ]
