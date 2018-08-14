# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassCourseInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('courseclassname', models.CharField(max_length=255, null=True, verbose_name=b'\xe7\x8f\xad\xe7\xba\xa7\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('coursestarttime', models.DateField(verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4')),
                ('courseendtime', models.DateField(verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4')),
                ('coursecount', models.IntegerField(verbose_name=b'\xe8\xaf\xbe\xe6\x97\xb6')),
                ('coursetime', models.TextField(null=True, verbose_name=b'\xe4\xb8\x8a\xe8\xaf\xbe\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('extrastatus', models.IntegerField(blank=True, null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe5\xbc\x80\xe7\x8f\xad\xe7\x8a\xb6\xe6\x80\x81', choices=[[2, b'\xe5\xb7\xb2\xe7\xbb\x93\xe8\xaf\xbe'], [3, b'\xe6\x9c\xaa\xe5\xbc\x80\xe7\x8f\xad'], [4, b'\xe5\xb7\xb2\xe5\x81\x9c\xe8\xaf\xbe']])),
                ('extrastatusreason', models.TextField(null=True, verbose_name=b'\xe5\xbc\x80\xe7\x8f\xad\xe7\x8a\xb6\xe6\x80\x81\xe5\x8e\x9f\xe5\x9b\xa0', blank=True)),
                ('coursedesc', models.TextField(null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('coursenotice', models.TextField(null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe5\x85\xac\xe5\x91\x8a', blank=True)),
            ],
            options={
                'verbose_name': '\u8bfe\u7a0b\u73ed\u8bfe\u7a0b\u4fe1\u606f',
                'verbose_name_plural': '\u8bfe\u7a0b\u73ed\u8bfe\u7a0b\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='ClassInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('classname', models.CharField(max_length=255, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe7\xbe\xa4\xe7\xb1\xbb\xe5\x9e\x8b', db_index=True)),
                ('starttime', models.DateField(null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe7\xbe\xa4\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('endtime', models.DateField(null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe7\xbe\xa4\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('classdesc', models.TextField(null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe7\xbe\xa4\xe7\xb1\xbb\xe5\x9e\x8b\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
            ],
            options={
                'verbose_name': '\u8bfe\u7a0b\u7fa4\u7c7b\u578b',
                'verbose_name_plural': '\u8bfe\u7a0b\u7fa4\u7c7b\u578b\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='CourseInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('coursename', models.CharField(max_length=255, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe5\x90\x8d\xe7\xa7\xb0', db_index=True)),
                ('coursedesc', models.TextField(null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
            ],
            options={
                'verbose_name': '\u8bfe\u7a0b\u4fe1\u606f',
                'verbose_name_plural': '\u8bfe\u7a0b\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='Cover',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('title', models.CharField(max_length=255, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98', db_index=True)),
                ('img', models.TextField(verbose_name=b'\xe5\x9b\xbe\xe7\x89\x87')),
                ('link', models.TextField(null=True, verbose_name=b'\xe9\x93\xbe\xe6\x8e\xa5')),
            ],
            options={
                'verbose_name': '\u5c01\u9762\u6d41',
                'verbose_name_plural': '\u5c01\u9762\u6d41',
            },
        ),
        migrations.CreateModel(
            name='EnrollCourseInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('status', models.IntegerField(verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[[0, b'\xe4\xb8\x8a\xe8\xaf\xbe'], [2, b'\xe9\x80\x80\xe8\xaf\xbe']])),
                ('coursecount', models.IntegerField(verbose_name=b'\xe8\xaf\xbe\xe6\x97\xb6\xe6\x95\xb0')),
                ('entrytime', models.DateField(null=True, verbose_name=b'\xe8\xbf\x9b\xe5\x85\xa5\xe4\xb8\x8a\xe8\xaf\xbe\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('realendtime', models.DateField(null=True, verbose_name=b'\xe7\xbb\x93\xe6\x9d\x9f\xe8\xaf\xbe\xe7\xa8\x8b\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('dropcoursetime', models.DateField(null=True, verbose_name=b'\xe9\x80\x80\xe8\xaf\xbe\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('dropcoursenote', models.TextField(null=True, verbose_name=b'\xe9\x80\x80\xe8\xaf\xbe\xe5\x8e\x9f\xe5\x9b\xa0', blank=True)),
                ('isrefund', models.IntegerField(verbose_name=b'\xe9\x80\x80\xe6\xac\xbe\xe7\x8a\xb6\xe6\x80\x81', choices=[[0, b'\xe6\x9c\xaa\xe9\x80\x80\xe6\xac\xbe'], [1, b'\xe5\xb7\xb2\xe9\x80\x80\xe6\xac\xbe']])),
                ('refundtime', models.DateField(null=True, verbose_name=b'\xe9\x80\x80\xe6\xac\xbe\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('refundmoney', models.CharField(max_length=255, null=True, verbose_name=b'\xe9\x80\x80\xe6\xac\xbe\xe9\x87\x91\xe9\xa2\x9d', blank=True)),
                ('refundnote', models.TextField(null=True, verbose_name=b'\xe9\x80\x80\xe6\xac\xbe\xe8\xaf\xb4\xe6\x98\x8e', blank=True)),
            ],
            options={
                'verbose_name': '\u62a5\u540d\u8868\u8bfe\u7a0b',
                'verbose_name_plural': '\u62a5\u540d\u8868\u8bfe\u7a0b',
            },
        ),
        migrations.CreateModel(
            name='EnrollCourseLeaveInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('leavereason', models.TextField(verbose_name=b'\xe5\x8e\x9f\xe5\x9b\xa0')),
                ('leavetime', models.DateField(verbose_name=b'\xe6\x97\xb6\xe9\x97\xb4')),
                ('courseindex', models.CharField(max_length=255, null=True, verbose_name=b'\xe7\xac\xac\xe5\x87\xa0\xe6\xac\xa1', blank=True)),
                ('enrollcourseinfo', models.ForeignKey(verbose_name=b'\xe5\x8d\x8f\xe8\xae\xae\xe8\xaf\xbe\xe7\xa8\x8b', to='info.EnrollCourseInfo')),
            ],
            options={
                'verbose_name': '\u8bfe\u7a0b\u9000\u8bfe\u4fe1\u606f',
                'verbose_name_plural': '\u8bfe\u7a0b\u9000\u8bfe\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='EnrollInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('no', models.CharField(db_index=True, max_length=255, null=True, verbose_name=b'\xe5\x8d\x8f\xe8\xae\xae\xe7\xbc\x96\xe5\x8f\xb7', blank=True)),
                ('totalcost', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x80\xbb\xe8\xb4\xb9\xe7\x94\xa8', blank=True)),
                ('discount', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x8a\x98\xe6\x89\xa3', blank=True)),
                ('realcost', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xae\x9e\xe6\x94\xb6\xe8\xb4\xb9\xe7\x94\xa8', blank=True)),
                ('paytime', models.DateField(null=True, verbose_name=b'\xe4\xbb\x98\xe6\xac\xbe\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('receiptno', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x94\xb6\xe6\x8d\xae\xe5\x8d\x95\xe5\x8f\xb7', blank=True)),
                ('posno', models.CharField(max_length=255, null=True, verbose_name=b'pos\xe5\x8d\x95\xe5\x8f\xb7', blank=True)),
                ('note', models.TextField(null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
                ('payee', models.ForeignKey(related_name='payee_user', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe6\x94\xb6\xe6\xac\xbe\xe4\xba\xba', blank=True, to='base.User', null=True)),
                ('user', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe4\xbf\xa1\xe6\x81\xaf', to='base.User')),
            ],
            options={
                'verbose_name': '\u534f\u8bae\u4fe1\u606f',
                'verbose_name_plural': '\u534f\u8bae\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='GradeInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('gradename', models.CharField(max_length=255, verbose_name=b'\xe5\xb9\xb4\xe7\xba\xa7\xe5\x90\x8d\xe7\xa7\xb0', db_index=True)),
                ('gradedesc', models.TextField(null=True, verbose_name=b'\xe5\xb9\xb4\xe7\xba\xa7\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
            ],
            options={
                'verbose_name': '\u5e74\u7ea7\u4fe1\u606f',
                'verbose_name_plural': '\u5e74\u7ea7\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='NewsBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('title', models.CharField(max_length=255, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98', db_index=True)),
                ('abstract', models.TextField(null=True, verbose_name=b'\xe6\x91\x98\xe8\xa6\x81', blank=True)),
                ('picture', models.TextField(null=True, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98\xe5\x9b\xbe\xe7\x89\x87', blank=True)),
                ('content', models.TextField(null=True, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9', blank=True)),
            ],
            options={
                'verbose_name': '\u65b0\u95fb',
                'verbose_name_plural': '\u65b0\u95fb',
            },
        ),
        migrations.CreateModel(
            name='OldData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('number', models.CharField(db_index=True, max_length=255, null=True, verbose_name=b'\xe5\x8d\x8f\xe8\xae\xae\xe7\xbc\x96\xe5\x8f\xb7', blank=True)),
                ('name', models.CharField(db_index=True, max_length=255, null=True, verbose_name=b'\xe5\xa7\x93\xe5\x90\x8d', blank=True)),
                ('sex', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab', blank=True)),
                ('school', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xad\xa6\xe6\xa0\xa1', blank=True)),
                ('grade', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xb9\xb4\xe7\xba\xa7', blank=True)),
                ('studentphonenumber', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xad\xa6\xe7\x94\x9f\xe7\x94\xb5\xe8\xaf\x9d', blank=True)),
                ('parentphonenumber', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xae\xb6\xe9\x95\xbf\xe7\x94\xb5\xe8\xaf\x9d', blank=True)),
                ('homeaddress', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xae\xb6\xe5\xba\xad\xe4\xbd\x8f\xe5\x9d\x80', blank=True)),
                ('courseclass', models.CharField(max_length=255, null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe7\x8f\xad', blank=True)),
                ('course1', models.CharField(max_length=255, null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b1', blank=True)),
                ('course2', models.CharField(max_length=255, null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b2', blank=True)),
                ('course3', models.CharField(max_length=255, null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b3', blank=True)),
                ('course4', models.CharField(max_length=255, null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b4', blank=True)),
                ('course5', models.CharField(max_length=255, null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b5', blank=True)),
                ('course6', models.CharField(max_length=255, null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b6', blank=True)),
                ('totalcost', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x80\xbb\xe8\x8a\xb1\xe8\xb4\xb9', blank=True)),
                ('discount', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x8a\x98\xe6\x89\xa3', blank=True)),
                ('realcost', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xae\x9e\xe9\x99\x85\xe8\x8a\xb1\xe8\xb4\xb9', blank=True)),
                ('payee', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x94\xb6\xe6\xac\xbe\xe4\xba\xba', blank=True)),
                ('receiptnumber', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x94\xb6\xe6\x8d\xae\xe5\x8f\xb7', blank=True)),
                ('posnumber', models.CharField(max_length=255, null=True, verbose_name=b'pos\xe5\x8d\x95\xe5\x8f\xb7', blank=True)),
                ('entrytime', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xbd\x95\xe5\x85\xa5\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('coursestarttime', models.CharField(max_length=255, null=True, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('theoryendtime', models.CharField(max_length=255, null=True, verbose_name=b'\xe7\x90\x86\xe8\xae\xba\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('realendtime', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xae\x9e\xe9\x99\x85\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('refundstate', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe6\x9c\x89\xe9\x80\x80\xe6\xac\xbe', blank=True)),
                ('refundmoney', models.CharField(max_length=255, null=True, verbose_name=b'\xe9\x80\x80\xe6\xac\xbe\xe9\x87\x91\xe9\xa2\x9d', blank=True)),
                ('refundtime', models.CharField(max_length=255, null=True, verbose_name=b'\xe9\x80\x80\xe6\xac\xbe\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('note', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
                ('paytime', models.CharField(max_length=255, null=True, verbose_name=b'\xe4\xbb\x98\xe6\xac\xbe\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('premoney', models.CharField(max_length=255, null=True, verbose_name=b'\xe9\xa2\x84\xe4\xbb\x98\xe6\xac\xbe', blank=True)),
                ('GradePeriod', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xb1\x8a\xe6\xac\xa1', blank=True)),
            ],
            options={
                'verbose_name': '\u5386\u53f2\u6570\u636e',
                'verbose_name_plural': '\u5386\u53f2\u6570\u636e',
            },
        ),
        migrations.CreateModel(
            name='PreEnrollInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('truename', models.CharField(max_length=20, verbose_name=b'\xe7\x9c\x9f\xe5\xae\x9e\xe5\xa7\x93\xe5\x90\x8d')),
                ('phone', models.CharField(max_length=100, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d')),
                ('preenrolltime', models.DateField(verbose_name=b'\xe9\xa2\x84\xe6\x8a\xa5\xe5\x90\x8d\xe6\x97\xb6\xe9\x97\xb4')),
                ('isoldstudent', models.IntegerField(verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xaf\xe8\x80\x81\xe5\xad\xa6\xe5\x91\x98')),
                ('getpath', models.TextField(verbose_name=b'\xe4\xbb\x8e\xe5\x93\xaa\xe9\x87\x8c\xe8\x8e\xb7\xe5\xbe\x97\xe7\x9a\x84\xe4\xbf\xa1\xe6\x81\xaf')),
                ('note', models.TextField(null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe9\xa2\x84\xe6\x8a\xa5\xe8\xaf\xbe\xe7\xa8\x8b', blank=True, to='info.ClassCourseInfo', null=True)),
                ('preenrollgrade', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe5\xb9\xb4\xe7\xba\xa7', blank=True, to='info.GradeInfo', null=True)),
            ],
            options={
                'verbose_name': '\u9884\u62a5\u540d\u4fe1\u606f',
                'verbose_name_plural': '\u9884\u62a5\u540d\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='SchoolInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('schoolname', models.CharField(max_length=255, verbose_name=b'\xe5\xad\xa6\xe6\xa0\xa1\xe5\x90\x8d\xe7\xa7\xb0', db_index=True)),
                ('schooldesc', models.TextField(null=True, verbose_name=b'\xe5\xad\xa6\xe6\xa0\xa1\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
            ],
            options={
                'verbose_name': '\u5b66\u6821\u4fe1\u606f',
                'verbose_name_plural': '\u5b66\u6821\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='SchoolYearInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f\xe6\x9d\x83\xe5\x80\xbc', editable=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('schoolyearname', models.CharField(max_length=255, verbose_name=b'\xe5\xad\xa6\xe5\xb9\xb4\xe5\x90\x8d\xe7\xa7\xb0', db_index=True)),
                ('schoolyeardesc', models.TextField(null=True, verbose_name=b'\xe5\xad\xa6\xe5\xb9\xb4\xe4\xbf\xa1\xe6\x81\xaf\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
            ],
            options={
                'verbose_name': '\u5b66\u5e74\u4fe1\u606f',
                'verbose_name_plural': '\u5b66\u5e74\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('newsbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='info.NewsBase')),
            ],
            options={
                'verbose_name': '\u65b0\u95fb',
                'verbose_name_plural': '\u65b0\u95fb',
            },
            bases=('info.newsbase',),
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('newsbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='info.NewsBase')),
            ],
            options={
                'verbose_name': '\u901a\u77e5\u516c\u544a',
                'verbose_name_plural': '\u901a\u77e5\u516c\u544a',
            },
            bases=('info.newsbase',),
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('newsbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='info.NewsBase')),
            ],
            options={
                'verbose_name': '\u79d1\u7814\u6d3b\u52a8',
                'verbose_name_plural': '\u79d1\u7814\u6d3b\u52a8',
            },
            bases=('info.newsbase',),
        ),
        migrations.AddField(
            model_name='preenrollinfo',
            name='preenrollschool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe5\xad\xa6\xe6\xa0\xa1', blank=True, to='info.SchoolInfo', null=True),
        ),
        migrations.AddField(
            model_name='enrollcourseinfo',
            name='enrollinfo',
            field=models.ForeignKey(verbose_name=b'\xe6\x8a\xa5\xe5\x90\x8d\xe8\xa1\xa8\xe4\xbf\xa1\xe6\x81\xaf', to='info.EnrollInfo'),
        ),
        migrations.AddField(
            model_name='enrollcourseinfo',
            name='gradecourseinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe6\x8a\xa5\xe5\x90\x8d\xe8\xaf\xbe\xe7\xa8\x8b\xe4\xbf\xa1\xe6\x81\xaf', blank=True, to='info.ClassCourseInfo', null=True),
        ),
        migrations.AddField(
            model_name='classinfo',
            name='schoolyearinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe5\xad\xa6\xe5\xb9\xb4\xe4\xbf\xa1\xe6\x81\xaf', blank=True, to='info.SchoolYearInfo', null=True),
        ),
        migrations.AddField(
            model_name='classcourseinfo',
            name='classinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b\xe7\xbe\xa4\xe4\xbf\xa1\xe6\x81\xaf', blank=True, to='info.ClassInfo', null=True),
        ),
        migrations.AddField(
            model_name='classcourseinfo',
            name='courseinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe8\xaf\xbe\xe7\xa8\x8b', blank=True, to='info.CourseInfo', null=True),
        ),
        migrations.AddField(
            model_name='classcourseinfo',
            name='gradeinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe5\xb9\xb4\xe7\xba\xa7\xe6\x88\x96\xe5\xb1\x8a\xe6\xac\xa1', blank=True, to='info.GradeInfo', null=True),
        ),
        migrations.AddField(
            model_name='classcourseinfo',
            name='teacherinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe8\x80\x81\xe5\xb8\x88\xe4\xbf\xa1\xe6\x81\xaf', blank=True, to='base.User', null=True),
        ),
    ]
