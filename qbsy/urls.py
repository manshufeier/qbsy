"""qbsy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import sys

from django.views.decorators.csrf import csrf_exempt

reload(sys)


class Sys:
    def setdefaultencoding(self):
        pass


sysx = sys
try:
    sysx.setdefaultencoding('utf8')
except:
    pass
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse
import base, xadmin
import info.views


def fav(request):
    return HttpResponseRedirect('/static/img/favicon.ico')


def goxadmin(request):
    return HttpResponseRedirect('/xadmin/')


from xadmin.views import LoginView
from info.api import wangeditor_imgupload, kingeditor_upload

urlpatterns = [
    url(r'^sladmin/', include(admin.site.urls)),
    url(r'^xadmin', include(xadmin.urls)),
    url(r'^$', include(xadmin.urls)),
    url(r'^api/', include(base.apiview.urlpatterns)),
    url(r'^wangeditor/uploadimg', csrf_exempt(wangeditor_imgupload)),
    url(r'^kingeditor/kingeditor_upload', csrf_exempt(kingeditor_upload)),
    url(r'^login.html', LoginView.as_view()),
    url(r'', include(base.urls)),
    url(r'', include(info.views.urlpatterns)),
]


def e404(request):
    return HttpResponse('<center><h1>oops, 404~</h1></center>')
