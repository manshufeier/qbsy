#!/bin/bash
echo 'site is stoping ...'
netstat -apn | grep 8081 | awk '{gsub("/python","",$7);print $7}' | xargs kill -9
echo 'svn is updating...'
svn up
echo 'restart ...'
echo 'make migrations ...'
python manage.py makemigrations
echo 'migrate ...'
python manage.py migrate
echo 'gunicorn is binding in 8081'
gunicorn -D -b 0.0.0.0:8081 qbsy.wsgi:application
echo 'restart successful!!!'
