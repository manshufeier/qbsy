# -*- coding: UTF-8 -*

from django.conf.urls import patterns
from django.core import paginator
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

from base.utils import gen_pager
from base.views import asview, PageView, AutoTemplView
from info.models import News, Notice, Research


@asview(logined=False)
class IndexPageView(PageView):
    def get(self, request):
        return self.render_to_response(request, 'xadmin/login.html', {})


@asview(logined=False)
class NormalNewsView(AutoTemplView):
    list_title=None
    model = None
    list_template_name = None
    detail_template_name = None

    def get(self, request, cururl, objid=None):
        if objid:
            item = self.model.objects.filter(pk=objid).first()
            lasts = self.model.objects.filter().order_by('-created')
            return self.render_to_response(request, templ=self.detail_template_name,
                                           cxt={'item': item, 'cururl': cururl, 'lasts': lasts,'list_title':self.list_title,'list_name':self.model.__name__.lower()})
        else:
            kw = request.GET.get('kw', '')
            query = self.model.objects.filter()
            if kw:
                query = query.filter(title__icontains=kw)
            pager = gen_pager(query, param=request.GET, size=12)
            items = [x for x in pager['items']]
            pager['items'] = items
            lasts = self.model.objects.filter().order_by('-published')
            return self.render_to_response(request, templ=self.list_template_name,
                                           cxt={'cururl': cururl, 'itemlist': items, 'pager': pager, 'kw': kw,
                                                'lasts': lasts,'list_title':self.list_title,'list_name':self.model.__name__.lower()})


urlpatterns = patterns('',
                       (r'^index.html$', IndexPageView.as_view()),
                       (r'^(news)/(\d*)',
                        NormalNewsView.as_view(model=News, list_template_name='list.html',
                                               detail_template_name='content.html',list_title="新闻中心")),
                       (r'^(notice)/(\d*)',
                        NormalNewsView.as_view(model=Notice, list_template_name='list.html',
                                               detail_template_name='content.html',list_title="通知公告")),
                       (r'^(research)/(\d*)',
                        NormalNewsView.as_view(model=Research, list_template_name='list.html',
                                               detail_template_name='content.html',list_title="科研成果")),
                       (r'', IndexPageView.as_view()),
                       )
