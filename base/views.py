# -*- coding: UTF-8 -*
'''
Copyright 2015 INRUAN Technology Co., Ltd. All rights reserved.

Created on 2015-7-22

@author: Robin
'''
import json
import os
import re

import django.views.generic.base as dj
from django.conf.urls import patterns
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Template, Context

from base.models import User
from base.siteinfo import get_gsite
from qbsy import settings

import sys

reload(sys)
sys.setdefaultencoding('utf8')


def json_filed_default(obj):
    import decimal
    import datetime
    import time
    from django.db.models.fields.files import ImageFieldFile
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    if isinstance(obj, datetime.datetime):
        return obj.timetuple()
    if isinstance(obj, datetime.date):
        return obj.timetuple()
    if isinstance(obj, time.struct_time):
        try:
            return {"timestamp": time.mktime(obj), "date": time.strftime('%Y-%m-%d', obj)}
        except:
            return {"date": time.strftime('%Y-%m-%d', obj)}
    if isinstance(obj, ImageFieldFile):
        if hasattr(obj, 'url'):
            return obj.url
        else:
            return ''
    from base.models import Role
    if isinstance(obj, User):
        return obj.simple_json
    if type(obj) in [User, Role]:
        return str(obj)
    return str(obj)


class BaseView(dj.View):
    me = None
    meid = None

    def __init__(self, **kwargs):
        dj.View.__init__(self, **kwargs)
        self.site = get_gsite()

    def get_session(self):
        return self.request.session

    def session_get(self, k):
        return self.get_session()[k] if k in self.get_session() else None

    def session_del(self, k):
        if k in self.get_session():
            del self.get_session()[k]

    def session_set(self, k, v):
        self.get_session()[k] = v

    def session_get_once(self, k):
        v = self.session_get(k)
        self.session_del(k)
        return v

    def get_me_modellist(self):
        import siteinfo
        import json
        me_oprations = json.loads(self.get_me().role.oprations)
        me_modellist = []
        for ops in siteinfo.site_oprations:
            for o in ops['oprations']:
                if str(o['k']) in me_oprations:
                    if ',' in o['value']:
                        m_list = o['value'].split(',')
                        for m in m_list:
                            me_modellist.append(m)
                    else:
                        me_modellist.append(o['value'])
        return me_modellist

    def check_opration(self, modelname):
        if self.get_me().id == 1 or self.get_me().username == 'admin':
            return True
        return modelname in self.get_me_modellist()

    def check_permission(self, modelname, permission):
        if self.get_me().id == 1 or self.get_me().username == 'admin':
            return True
        permission_dic = self.get_permission()
        return permission_dic.get(modelname).get(permission) if permission_dic else None

    def check_op_index(self, index):
        return index in [int(op) for op in json.loads(self.get_me().role.oprations)]

    def get_me_oprations(self):
        import siteinfo
        s_oprations = siteinfo.site_oprations
        for op in s_oprations:
            for ops in op['oprations']:
                if (not self.check_op_index(ops['k'])) and not self.get_me().isadmin:
                    ops['isindexshow'] = False
                else:
                    ops['isindexshow'] = True
                if not ops.get('isshow'):
                    ops['isindexshow'] = False
                if ops['isme']:
                    import re
                    p = re.compile('(&q__user_id=[1-9]+&user_id=[1-9]+)')
                    ops['href'] = p.sub('', ops['href']) + '&q__user_id=' + str(
                        self.get_me().id) + '&user_id=' + str(self.get_me().id)
                if not ops['isadd']:
                    ops['href'] = ops['href'] + '&isadd=-1'
                if not ops['isdelete']:
                    ops['href'] = ops['href'] + '&isdelete=-1'
            op['oplen'] = len([o for o in op['oprations'] if o['isindexshow']])
        return s_oprations

    def get_meid(self):
        sme = self.session_get('me')
        if sme:
            return sme['id']
        else:
            return None

    def get_me(self):
        if self.me:
            return self.me
        self.meid = self.get_meid()
        if self.meid:
            self.me = User.objects.filter(
                pk=self.meid, status=User.STATUS_NORMAL).first()
            if self.me:
                self.session_set('me', self.me.get_json())
            else:
                self.session_del('me')
            return self.me
        else:
            return None

    def get_roles(self):
        sme = self.session_get('me')
        if sme:
            return sme['roles']
        else:
            me = self.get_me()
            if me:
                return me.get_roles()
        return []

    def dispatch(self, request, *args, **kwargs):
        self.me = None
        self.meid = None
        return dj.View.dispatch(self, request, *args, **kwargs)

    def is_www(self):
        ua = self.request.META['HTTP_USER_AGENT'].upper()
        return 'MOBILE' not in ua

    def getModel(self, modelname):
        return self.site.getModel(modelname)

    def has_role(self, role):
        return role in self.get_roles()

    def get_model_permission(self):
        modelname = self.request.GET.get('modelname')
        permission_dic = self.get_permission()
        if self.get_me().isadmin:
            return {
                'is_add': True,
                'is_edit': True,
                'is_delete': True,
                'is_export': True,
                'is_top': True,
                'is_self': True
            }
        return permission_dic.get(modelname) if permission_dic else None

    def get_permission(self):
        if not self.get_me():
            return None
        model_permission = self.get_me().role.model_permission
        return json.loads(model_permission) if model_permission else None


def asapi(logined=True, userrole=None, args=None, token=None):
    def _func(func):
        def __func(self, *args, **kvagrs):
            return func(self, *args, **kvagrs)

        import inspect
        setattr(__func, 'api', True)
        setattr(__func, 'argspec', inspect.getargspec(func))
        setattr(__func, 'doc', inspect.getdoc(func))
        setattr(__func, 'logined', logined)
        setattr(__func, 'userrole', userrole)
        setattr(__func, 'token', token)
        return __func

    return _func


class ApiView(BaseView):
    def api_response(self, v):
        res = HttpResponse(json.dumps(
            v, default=json_filed_default), content_type="text/json")
        if 'login' in self.request.path or 'logout' in self.request.path:
            import time
            res.set_cookie('_timestamp', str(time.time()))
        return res

    def warpvalue(self, v):
        if type(v) in (unicode, str):
            return u'"%s"' % v.replace('"', '\\"')
        else:
            return json.dumps(v)

    def doc(self, request):
        apis = []
        for an in dir(self.__class__):
            at = getattr(self.__class__, an)
            if hasattr(at, 'logined'):
                apifun = at
                token = getattr(apifun, 'token')
                logined = getattr(apifun, 'logined')
                userrole = getattr(apifun, 'userrole')
                argspec = getattr(apifun, 'argspec')
                doc = getattr(apifun, 'doc')
                funcagrs = argspec.args
                defaults = argspec.defaults
                args = []
                argslen = len(funcagrs) - (len(defaults)
                                           if defaults else 0) - 1
                for i, k in enumerate(funcagrs[1:]):
                    arg = {
                        'name': k
                    }
                    if i >= argslen:
                        arg['default'] = self.warpvalue(defaults[i - argslen])
                        arg['hasdefault'] = True
                    args.append(arg)
                apis.append({
                    'token': token,
                    'name': an,
                    'doc': doc,
                    'args': args,
                    'logined': logined,
                    'userrole': userrole if type(userrole) in (list, tuple, set) else (
                        [userrole, ] if userrole else None)
                })
        cxt = Context({'api_url': getattr(self, 'get_host') if hasattr(self, 'get_host') else None, 'apis': apis,
                       'template_name': 'utils/apidoc.html'})
        return HttpResponse(
            content=Template(open(os.path.join(settings.BASE_DIR, 'templates', 'utils', 'apidoc.html')).read()).render(
                cxt))

    def get(self, request, apiname, *k, **ks):
        from utils import ex, Data, ApiException
        self.me = None
        self.meid = None
        try:
            if apiname == 'doc.html' or not apiname:
                return self.doc(request)
            if not apiname:
                raise ex(u"接口不能为空")
            try:
                apifun = getattr(self, apiname)
            except:
                raise ex(u"不存在接口 %s" % apiname)

            needlogin = getattr(apifun, 'logined')
            userrole = getattr(apifun, 'userrole')

            token = getattr(apifun, 'token')

            if needlogin and not self.get_meid():
                raise ex(u'你还未登录哦')

            if userrole and not self.get_me().checkrole(userrole):
                raise ex(u'用户权限不足')

            kvargs = {}
            param = {}
            param.update(request.REQUEST)
            argspec = getattr(apifun, 'argspec')
            funcagrs = argspec.args
            defaults = argspec.defaults

            if defaults:
                for i, v in enumerate(funcagrs[-len(defaults):]):
                    kvargs[v] = defaults[i]
            if len(funcagrs):
                param['_param'] = param
                argslen = len(funcagrs) - (len(defaults)
                                           if defaults else 0) - 1
                missargs = []
                for i, k in enumerate(funcagrs[1:]):
                    if k in param:
                        kvargs[k] = param[k]
                    elif i < argslen:
                        missargs.append(k)
                if missargs:
                    raise ex(u'缺失参数: %s' % (', '.join(missargs)))

            if token:
                if not kvargs.get('token'):
                    raise ex(u'你还未登录哦')
                else:
                    nuser = self.get_user_by_token(kvargs.get('token'))
                    if not nuser:
                        raise ex(u'你还未登录哦')

            res = apifun(**kvargs)
            if isinstance(res, Data):
                res = {"code": 0, "data": res.data}
            elif res != None:
                res = {"code": 0, "data": res}
                if apiname == 'check_update':
                    res = res['data']
            if not res:
                res = {"code": 0}
            return self.api_response(res)
        except ApiException, e:
            return self.api_response(e.args[0])

    def post(self, request, *k, **ks):
        return self.get(request, *k, **ks)

    def delete(self, request, *k, **ks):
        return self.get(request, *k, **ks)

    def put(self, request, *k, **ks):
        return self.get(request, *k, **ks)


def dispatch(self, request, *args, **kwargs):
    if self.site.setting.get('sitemaintaining') and not request.path.startswith('/xadmin'):
        return self.render_to_response(request, templ='error.html',
                                       cxt={'stopback': True, 'err': self.site.setting['sitemaintainingtext']})
    if (self.logined or self.userrole) and not self.get_meid():
        self.session_set('logingoto', request.path)
        return HttpResponseRedirect("/login.html")
    if self.userrole:
        me = self.get_me()
        if not me.checkrole(self.userrole):
            return self.render_to_response(request, templ='error.html', cxt={'err': u'无权访问!'})
    if not self.site.setting.get('sys_debug'):
        try:
            res = BaseView.dispatch(self, request, *args, **kwargs)
        except:
            res = self.render_to_response(
                request, templ='error.html', cxt={'err': u'访问出错!'})
    else:
        res = BaseView.dispatch(self, request, *args, **kwargs)
    return res


def asview(logined=True, userrole=None):
    def _auth(view, *args, **kvagrs):
        if logined or userrole:
            setattr(view, 'logined', True)
        if userrole:
            setattr(view, 'userrole', userrole)
        return view

    return _auth


class PageView(BaseView):
    logined = False
    userrole = None
    content_type = 'text/html'
    template_name = None

    def dispatch(self, request, *args, **kwargs):
        return dispatch(self, request, *args, **kwargs)

    def render(self, request, templ, cxt):
        if cxt == None:
            cxt = {}
        cxt['template_name'] = templ
        cxt['site'] = self.site
        cxt['view'] = self
        cxt['view_name'] = self.__class__.__name__
        cxt['me'] = self.get_me()
        cxt['STATIC_URL'] = '/static/'
        cxt['kw'] = request.GET.get('kw', '')
        cxt['request'] = request
        if self.get_me() and self.request.GET.get('modelname'):
            cxt['mp'] = self.get_model_permission()

        templpath = settings.TEMPLATE_BASE_DIR
        from django.conf import settings as gsettings
        from django.template.backends.django import DjangoTemplates
        if templpath not in self.site.template_engines:
            self.site.template_engines[templpath] = DjangoTemplates({
                'APP_DIRS': False,
                'DIRS': [templpath],
                'NAME': 'django',
                'OPTIONS': {
                    'allowed_include_roots': gsettings.ALLOWED_INCLUDE_ROOTS,
                    'context_processors': gsettings.TEMPLATE_CONTEXT_PROCESSORS,
                    'debug': gsettings.TEMPLATE_DEBUG,
                    'loaders': gsettings.TEMPLATE_LOADERS,
                    'string_if_invalid': gsettings.TEMPLATE_STRING_IF_INVALID,
                }
            })
        ng = self.site.template_engines[templpath]
        content = ng.get_template(templ).render(Context(cxt))
        return HttpResponse(content=content)

    def render_to_response(self, request, templ=None, cxt=None):
        if templ == None:
            templ = self.get_template_name()
        return self.render(request, templ, cxt)

    def get_template_name(self):
        return self.template_name

    def get(self, request):
        return self.render_to_response(request)


class AutoTemplView(PageView):
    autotemplage = True

    def render(self, request, templ, cxt):
        if self.site.autotemplage and self.autotemplage:
            templ = 'www/%s' % templ
        return PageView.render(self, request, templ, cxt)


class RequestTempView(AutoTemplView):
    def get(self, request, templ=None):
        return self.render_to_response(request, templ)


class WapPageView(AutoTemplView):
    def is_wap(self):
        return True


class WebPageView(AutoTemplView):
    def is_www(self):
        return True

    def is_wap(self):
        return False


class StaticTemplateView(AutoTemplView):
    def get(self, request, templ):
        return self.render_to_response(request, templ=templ)


class MediaHandleView(dj.View):
    document_root = None
    rwh = re.compile('(\d+)x(\d+)')

    def handleImage(self, rawpath, newpath, arg):
        try:
            from PIL import Image
            im = Image.open(rawpath)
            w, h = im.size
            if arg == 'small':
                k = float(h) / float(w)
                w = 200
                h = int(w * k)
                newimg = im.resize((w, h), )
                newimg.save(newpath, quality=100)
                return newpath
            else:
                rs = MediaHandleView.rwh.findall(arg)
                if rs:
                    r = rs[0]
                    #                     im.thumbnail((int(r[0]),int(r[1])))
                    nw = int(r[0])
                    nh = int(r[1])
                    k = float(h) / float(w)
                    nk = float(nh) / float(nw)
                    if nk > k:
                        ch = h
                        cw = ch / nk
                    elif nk < k:
                        cw = w
                        ch = cw * nk
                    else:
                        cw = w
                        ch = h
                    cw, ch = int(cw), int(ch)
                    if cw != w or ch != h:
                        r = ((w - cw) / 2, (h - ch) / 2, w - (w - cw) / 2, h - (h - ch) / 2)
                        im = im.crop(r)

                    newimg = im.resize((nw, nh))
                    newimg.save(newpath, quality=100)
                    return newpath
                else:
                    return rawpath
        except Exception, e:
            print '%s : %s' % (e, rawpath)
            return rawpath

    def get(self, request, path):
        import posixpath
        from urllib import unquote
        arg = request.GET.get('type', '')
        path = posixpath.normpath(unquote(path)).lstrip('/')
        abspath = os.path.join(self.document_root, *path.split('/'))
        print arg, ",", path, ",", abspath
        if os.path.isfile(abspath):
            newabspath = abspath
            if arg:
                document_root, path = os.path.split(abspath)
                name, ext = os.path.splitext(path)
                newabspath = os.path.join(document_root, u'%s-%s%s' % (name, arg, ext))
                if request.GET.get('force') or not os.path.isfile(newabspath) or os.stat(abspath).st_mtime > os.stat(
                        newabspath).st_mtime:
                    abspath = self.handleImage(abspath, newabspath, arg)
                else:
                    abspath = newabspath
            from django.views import static
            document_root, path = os.path.split(abspath)
            res = static.serve(request, path, document_root, settings.DEBUG)
            if 'attname' in request.GET:
                res['Content-Disposition'] = 'attachment;filename="{0}"'.format(request.GET['attname'])
                res['Content-Type'] = 'application/octet-stream'
            return res
        else:
            from django.http import Http404
            raise Http404


urlpatterns = patterns('',
                       (r'^(.*\.html)$', StaticTemplateView.as_view()),
                       (r'^media/(?P<path>.*)$',
                        MediaHandleView.as_view(document_root=os.path.join(settings.BASE_DIR, 'media'))),
                       )
