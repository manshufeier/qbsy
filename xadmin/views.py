# -*- coding: UTF-8 -*
'''
Copyright 2015 INRUAN Technology Co., Ltd. All rights reserved.

Created on 2016-01-31

@author: Robin
'''
from django.conf.urls import patterns

from base.views import PageView, RequestTempView, asview


@asview(logined=False)
class LoginView(PageView):
    template_name = 'xadmin/login2.html'


@asview(logined=True)
class LoginedView(PageView):
    def render_to_response(self, request, templ=None, cxt=None):
        if cxt == None:
            cxt = {}
        cxt['me'] = self.get_me()
        #         cxt['roles'] = Role.objects.filter()
        return PageView.render_to_response(self, request, templ=templ, cxt=cxt)


@asview(userrole='admin')
class AdminView(PageView):
    def is_wap(self):
        return False

    def is_www(self):
        return True

    def is_weixin(self):
        return False

    def render_to_response(self, request, templ=None, cxt=None):
        if cxt == None:
            cxt = {}
        cxt['me'] = self.get_me()
        return PageView.render_to_response(self, request, templ=templ, cxt=cxt)

    def dispatch(self, request, *args, **kwargs):
        if self.site.setting.get('xadmindisable') and request.path != '/xadmin/setting.html':
            return self.render_to_response(request, templ='xadmin/error.html', cxt={'err': u'后台管理功能暂时被禁用!'})
        return PageView.dispatch(self, request, *args, **kwargs)


class XAdminRequestTempView(RequestTempView):
    autotemplage = False

    def get(self, request, templ):
        cxt = dict([(k, request.GET[k]) for k in request.GET])
        return self.render_to_response(request, templ='xadmin/%s' % templ, cxt=cxt)


urlpatterns = patterns('',
                       (r'^/login.html$', LoginView.as_view()),
                       (r'^/welcome.html$', LoginedView.as_view(template_name='xadmin/welcome.html')),
                       (r'^/(\S+.html)$', XAdminRequestTempView.as_view()),
                       (r'', LoginedView.as_view(template_name='xadmin/index.html')),
                       )
