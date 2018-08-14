# -*- coding: UTF-8 -*
'''
Copyright 2016 INRUAN Technology Co., Ltd. All rights reserved.

Created on 2016-01-31

@author: Robin
'''

from django.db import models
import json
import utils
from base import config


def _(v):
    return v


class CallMixin:
    def __getattr__(self, name):
        '''
        方法注入
        '''
        if name.startswith("call__"):

            sps = name.split("__")
            fname = sps[1]
            try:
                #                 print fname
                func = getattr(self, fname)
            except:
                raise Exception("get method failed: %s(%s)" % (name, fname))
            args = sps[2:]
            return func(*args)
        return getattr(super(BaseModel, self), name)  # super(BaseModel, self).__getattr__(name)

    pass


class BaseModel(models.Model):
    ordering = models.IntegerField(_('排序权值'), default=0, db_index=True, editable=False)
    created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated = models.DateTimeField(_('修改时间'), auto_now=True)

    def __getattr__(self, name):
        '''
        方法注入
        '''
        if name.startswith("call__"):

            sps = name.split("__")
            fname = sps[1]
            try:
                func = getattr(self, fname)
            except:
                raise Exception("run method failed: %s" % name)
            args = sps[2:]
            return func(*args)
        return getattr(super(BaseModel, self), name)  # super(BaseModel, self).__getattr__(name)

    class Meta:
        abstract = True
        ordering = ['-ordering', '-id']

    def get_json_by_fields(self, fields):
        res = self.get_json()
        if fields:
            res_new = {}
            for f in fields:
                res_new[f] = res[f]
            return res_new
        else:
            return res

    def get_select_json(self):
        return {
            'id': self.id,
            'name': self.showname
        }

    def get_base_json(self):
        return {
            'name':self.showname,
            'id': self.id,
            'ordering': self.ordering,
            'showname': self.showname,
            'created_text': self.created.strftime("%Y-%m-%d %H:%M:%S")
        }

    @classmethod
    def get_fields(clz):
        return clz._meta.fields

    @classmethod
    def get_allfields(clz):
        return [f.name for f in clz.get_fields()]

    @classmethod
    def get_editfields(clz):
        return [f.name for f in clz.get_fields() if f.editable and not f.primary_key]

    @classmethod
    def get_dictfields(cls, full=False):
        arr = []
        for f in cls.get_fields():
            if f.editable and not f.primary_key:
                fd = {
                    'name': f.name + "_id" if hasattr(f, 'rel') and hasattr(f.rel, 'to') else f.name,
                    'editable': f.editable and not f.primary_key,
                    'value': f.get_default(),
                    'type': f.__class__.__name__,
                    'max_length': f.max_length,
                    'required': not (f.blank or f.null),
                    'verbose_name': f.verbose_name,
                    'choices': f.choices,
                    'relmodel': (f.rel.to.__name__ if hasattr(f.rel.to, '__name__') else f.rel.to) if hasattr(f,
                                                                                                              'rel') and hasattr(
                        f.rel, 'to') else None
                }
                if full:
                    fd['field'] = f
                arr.append(fd)
        return arr


class ChildrenModelMixin(object):
    @property
    def children(self):
        return self.get_children()

    @property
    def all_children(self):
        ids = self.get_subidarray()
        ids.remove(self.id)
        return type(self).objects.filter(pk__in=ids)

    def get_children(self, **filters):
        return type(self).objects.filter(parent_id=self.id, **filters).select_related('parent')

    @property
    def gap_children(self):
        return type(self).objects.filter(
            parent_id__in=[v[0] for v in type(self).objects.filter(parent_id=self.id).values_list('id')])

    def get_subidarray(self):
        subids = json.loads(self.subids)['v'] if type(self.subids) != type([]) else self.subids
        return subids

    def get_full(self):
        a = self
        addrs = [a]
        while a.parent_id:
            a = a.parent
            addrs.append(a)
        addrs.reverse()
        return addrs

    def refresh_subids(self):
        '''刷新自身以及父节点subid'''
        clz = self.__class__
        subids = []
        for c in clz.objects.filter(parent=self):
            subids += c.get_subidarray()
            subids.append(c.id)
        self.subids = subids
        self.save()
        ids = [i for i in subids]
        ids.append(self.id)

        p = self.parent
        while p:
            p.subids = list(set(p.get_subidarray() + ids))
            p.save()
            p = p.parent

    def before_delete(self):
        '''节点删除前调用'''
        ids = [i for i in self.get_subidarray()]
        ids.append(self.id)

        p = self.parent
        ids = set(ids)
        while p:
            p.subids = list(set(p.get_subidarray()) - ids)
            p.save()
            p = p.parent

    def __unicode__(self):
        return '%s%s%s' % ('|' if self.level else '', '-' * self.level, self.name)


import siteinfo


def get_name_from_opration(k):
    for op in siteinfo.site_oprations:
        for ops in op['oprations']:
            if ops['k'] == int(k):
                return {'name': ops['name']}


class Role(BaseModel):
    role_write = 'admin'
    name = models.CharField(_('角色名称'), max_length=255)
    role = models.CharField(_('角色权限'), max_length=255)
    oprations = models.TextField(_('操作'))
    model_permission = models.TextField(verbose_name='模型权限', null=True, blank=True)

    @property
    def roles(self):
        return [s.strip() for s in self.role.split(',') if s.strip()] if self.role else []

    @property
    def showname(self):
        return self.name

    def get_json(self):
        return {
            'ordering': self.ordering,
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'userlist': [u.get_json() for u in User.objects.filter(role=self)],
            'oprations': self.oprations,
            'opration_list': [get_name_from_opration(k) for k in json.loads(self.oprations)],
            'model_permission': self.model_permission
        }

    showitem = {
        'showfield': [
            utils.gen_show_field('id', 'id', 'text'),
            utils.gen_show_field('角色名称', 'name', 'text'),
            utils.gen_show_field('角色', 'role', 'text'),
            utils.gen_show_field('用户列表', 'userlist', 'strlist'),
            utils.gen_show_field('角色权限', 'opration_list', 'strlist')
        ]
    }

    edititem = [
        utils.gen_edit_field('角色描述', 'name', config.EDIT_TEXT, verify=config.VERIFY_REQUIRED,
                             helptext='标明该角色的管理作用域，用中文描述'),
        utils.gen_edit_field('角色', 'role', config.EDIT_TEXT, verify=config.VERIFY_REQUIRED,
                             helptext='请输入角色的名称,如admin,teacher'),
        utils.gen_edit_field('角色权限', 'oprations', 'rolecheckbox', helptext='给角色分配权限'),
        utils.gen_edit_field('模型权限', 'model_permission', 'modelconfig')
    ]

    def __unicode__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name = _('角色')
        verbose_name_plural = _('角色')
        app_label = 'base'


class User(BaseModel):
    default_salt = 'inruan.com'
    role = models.ForeignKey(to=Role, verbose_name=_('所属角色'), null=True, blank=True, on_delete=models.SET_NULL)
    username = models.CharField(_('登录帐号'), max_length=32, db_index=True, null=False, unique=True)
    password = models.CharField(_('加密密码'), max_length=32, null=False)

    truename = models.CharField(_('真实姓名'), db_index=True, max_length=128, null=True, blank=True)
    nickname = models.CharField(_('昵称'), db_index=True, max_length=255)
    email = models.EmailField(_('电子邮件'), db_index=True, null=True, blank=True)
    phone = models.CharField(_('手机号码'), db_index=True, null=True, max_length=64, blank=True)
    homephone = models.CharField(_('家庭电话'), db_index=True, null=True, blank=True, max_length=64)
    icon = models.CharField(_('用户头像'), max_length=255, null=True, blank=True)
    userinfo = models.TextField(_('个人简介'), null=True, blank=True)
    school = models.ForeignKey(verbose_name='学校', to='info.SchoolInfo', null=True, blank=True,
                               on_delete=models.SET_NULL)
    grade = models.ForeignKey(verbose_name='年级或届次', to='info.GradeInfo', null=True, blank=True,
                              on_delete=models.SET_NULL)
    entryexamscore = models.FloatField(verbose_name='高考分数', null=True, blank=True)
    entryschool = models.TextField(verbose_name='录取学校', null=True, blank=True)
    STATUS_NORMAL = 0
    STATUS_CANCELED = -1
    STATUS_CHOICES = ((STATUS_NORMAL, "正常"), (STATUS_CANCELED, "已锁定"))
    STATUS_MAP = dict(STATUS_CHOICES)
    status = models.IntegerField(_('状态'), default=STATUS_NORMAL, choices=STATUS_CHOICES, editable=False)

    @property
    def status_text(self):
        return User.STATUS_MAP[self.status] if self.status in User.STATUS_MAP else None

    salt = models.CharField(_('密码盐巴'), default=default_salt, max_length=32, blank=True)

    token = models.CharField(_('访问令牌'), db_index=True, max_length=128, null=True, blank=True)

    rolelist = models.TextField(_('用户权限'), default=[], editable=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if len(self.password) != 32:
            import hashlib, time
            self.salt = hashlib.md5(str(time.time()) + self.salt).hexdigest()
            self.password = User.pwdhash(self.password, self.salt)
        return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using,
                                 update_fields=update_fields)

    @property
    def showname(self):
        return self.truename or self.username or self.phone

    @staticmethod
    def pwdhash(pwd, salt):
        import hashlib
        return hashlib.md5(hashlib.md5(pwd).hexdigest() + hashlib.md5(salt).hexdigest()).hexdigest()

    def __unicode__(self):
        return self.showname

    def get_json(self):
        return {
            'ordering': self.ordering,
            'id': self.id,
            'showname': self.showname,
            'username': self.username,
            'icon': self.icon,
            'roles': self.get_roles(),
            'role_id': self.role.id if self.role else '',
            'truename': self.truename,
            'name': self.showname,
            'phone': self.phone,
            'status_text': self.status_text,
            'email': self.email,
            'role_name': self.role.name if self.role else '',
            'nickname': self.nickname,
            'userinfo': self.userinfo,
            'homephone': self.homephone,
            'school': None,
            'school_name': utils.get_foreignkey_value(self.school, 'schoolname'),
            'school_id': utils.get_foreignkey_value(self.school, 'id'),
            'grade': None,
            'grade_name': utils.get_foreignkey_value(self.grade, 'gradename'),
            'grade_id': utils.get_foreignkey_value(self.grade, 'id'),
            'entryexamscore': self.entryexamscore,
            'entryschool': self.entryschool
        }

    def get_list_json(self):
        res = self.get_base_json()
        res.update({
            'username': self.username,
            'truename': self.truename,
            'nickname': self.nickname,
            'phone': self.phone,
            'homephone': self.homephone,
            'school_name': utils.get_foreignkey_value(self.school, 'showname'),
            'grade_name': utils.get_foreignkey_value(self.grade, 'showname'),
            'entryexamscore': self.entryexamscore,
            'entryschool': self.entryschool,
            'enrollinfo_link': "B.addWindowTab('" + self.showname + "协议信息','/xadmin/modellist.html?modelname=EnrollInfo&q__user_id=" + str(
                self.id) + "')",
            'courseinfo_link': "B.addWindowTab('" + self.showname + "课程信息','/xadmin/modellist.html?modelname=EnrollCourseInfo&q__enrollinfo__user_id=" + str(
                self.id) + "&isadd=-1')",
            'dropcourse_link': "B.addWindowTab('" + self.showname + "退课信息','/xadmin/modellist.html?modelname=EnrollCourseInfo&q__enrollinfo__user_id=" + str(
                self.id) + "&isadd=-1&q__status=2')",
            'teachercourse_link': "B.addWindowTab('" + self.showname + "课程信息','/xadmin/modellist.html?modelname=ClassCourseInfo&q__teacherinfo_id=" + str(
                self.id) + "&isadd=-1')",
            'examrecord_link': "B.addWindowTab('" + self.showname + "成绩记录','/xadmin/modellist.html?modelname=Exam&q__user_id=" + str(
                self.id) + "')",
            'teacher_assistant_link': "B.addWindowTab('管理{0}教辅课程信息','/xadmin/modellist.html?modelname=TeacherAssistantCourse&q__user_id={1}');".format(
                self.showname, self.id),
        })
        return res

    showitem = {
        'showfield': [
            utils.gen_show_field('用户名', 'username', 'text'),
            utils.gen_show_field('真实姓名', 'truename', 'text'),
            utils.gen_edit_field('昵称', 'nickname', 'text'),
            utils.gen_show_field('电话号码', 'phone', 'html'),
            utils.gen_show_field('家庭电话', 'homephone', 'text', showkey='q__role__id', showvalue=3),
            utils.gen_show_field('学校', 'school_name', 'text', showkey='q__role__id', showvalue=3),
            utils.gen_show_field('年级', 'grade_name', 'text', showkey='q__role__id', showvalue=3),
            utils.gen_show_field('高考分数', 'entryexamscore', config.SHOW_TEXT, showkey='q__role__id', showvalue=3),
            utils.gen_show_field('录取学校', 'entryschool', config.SHOW_TEXT, showkey='q__role__id', showvalue=3)
        ],
        'verbose_name': '用户信息',
        'linkfield': [
            utils.gen_link_field('teachercourse_link', '课程信息', showkey='q__role__id', showvalue=2),
            utils.gen_link_field('teacher_assistant_link', '管理教辅课程', showkey='q__role__id', showvalue=6),
            utils.gen_link_field(None, '<span style="color:gray;">&nbsp;|&nbsp;</span>', islink=False,
                                 showkey='q__role__id', showvalue=3),
            utils.gen_link_field('enrollinfo_link', '协议信息', showkey='q__role__id', showvalue=3),
            utils.gen_link_field('courseinfo_link', '课程信息', showkey='q__role__id', showvalue=3),
            utils.gen_link_field(None, '<br>', islink=False, showkey='q__role__id', showvalue=3),
            utils.gen_link_field('dropcourse_link', '退课信息', showkey='q__role__id', showvalue=3),
            utils.gen_link_field('examrecord_link', '成绩记录', showkey='q__role__id', showvalue=3)
        ],
        'isexport': True
    }

    edititem = [
        utils.gen_edit_field('角色', 'role', 'select', helptext='用户角色', disabled=True, defaultselect_q='q__role__id'),
        utils.gen_edit_field('用户名', 'username', 'text', verify='required|username', helptext='输入用户名，作为用户登录系统的用户账号',
                             defaultselect_q='username'),
        utils.gen_edit_field('密码', 'password', 'password', helptext='输入用户的密码', verify='password',
                             defaultselect_q='password'),
        utils.gen_edit_field('用户头像', 'icon', 'usericon', helptext='选择用户头像'),
        utils.gen_edit_field('真实姓名', 'truename', 'text', helptext='输入用户的真实姓名,管理用', verify='required',
                             defaultselect_q='truename'),
        utils.gen_edit_field('昵称', 'nickname', 'text', helptext='输入昵称，公开', verify='required',
                             defaultselect_q='truename'),
        utils.gen_edit_field('联系电话', 'phone', 'text', helptext='请输入联系电话', verify='phone'),
        utils.gen_edit_field('学校', 'school', 'select', helptext='选择学校', modelname='SchoolInfo', showkey='q__role__id',
                             showvalue=3, defaultselect_q='q__school__id'),
        utils.gen_edit_field('年级或届次', 'grade', 'select', helptext='选择年级或届次', modelname='GradeInfo',
                             showkey='q__role__id', showvalue=3, defaultselect_q='q__grade__id'),
        utils.gen_edit_field('家庭电话', 'homephone', 'text', helptext='请输入家庭联系电话', verify='phone',
                             defaultselect_q='phone', showkey='q__role__id', showvalue=3),
        utils.gen_edit_field('电子邮件', 'email', 'text', helptext='输入电子邮件', verify='email'),
        utils.gen_edit_field('个人简介', 'userinfo', 'kingeditor', helptext='输入个人简介', showkey='q__role__id', showvalue=2),
        utils.gen_edit_field('高考分数', 'entryexamscore', config.EDIT_TEXT, helptext='请输入该学生的高考分数',
                             verify=config.VERIFY_FLOAT, showkey='q__role__id', showvalue=3),
        utils.gen_edit_field('录取学校', 'entryschool', config.EDIT_TEXT, helptext='请输入该学生的录取学校', showkey='q__role__id',
                             showvalue=3)
    ]

    exportlist = [
        utils.gen_export_field('角色', 'role_name'),
        utils.gen_export_field('用户名', 'username'),
        utils.gen_export_field('用户头像', 'icon'),
        utils.gen_export_field('真实姓名', 'truename'),
        utils.gen_export_field('昵称', 'nickname'),
        utils.gen_export_field('联系电话', 'phone'),
        utils.gen_export_field('家庭联系电话(学生)', 'homephone'),
        utils.gen_export_field('电子邮件', 'email'),
        utils.gen_export_field('个人简介', 'userinfo'),
        utils.gen_export_field('学校(学生)', 'school_name'),
        utils.gen_export_field('年级或届次(学生)', 'grade_name'),
        utils.gen_export_field('高考分数', 'entryexamscore'),
        utils.gen_export_field('录取学校', 'entryschool')
    ]

    def get_roles(self):
        roles = ['user']
        if self.username == 'admin' or self.id == 1:
            roles.append('admin')
        if self.role_id:
            roles = roles + self.role.roles
        return list(set(roles))

    @property
    def roles(self):
        return self.get_roles()

    @property
    def iscollector(self):
        return 'collector' in self.roles

    @property
    def isadmin(self):
        return 'admin' in self.roles

    @property
    def isteacher(self):
        return 'teacher' in self.roles

    @property
    def isstudent(self):
        return 'student' in self.roles

    @property
    def isreception(self):
        return 'reception' in self.roles

    @property
    def is_super_reception(self):
        return 'super_reception' in self.roles

    @property
    def is_teacher_assistant(self):
        return 'teacher_assistant' in self.roles

    @property
    def roles_names(self):
        arr = (
            ('admin', u'管理员')
        )
        roles = self.roles
        names = []
        for k, v in arr:
            if k in roles:
                names.append(v)
        return names

    @property
    def role_text(self):
        return self.role.name if self.role else None

    def checkrole(self, roles):
        if type(roles) != list:
            roles = [roles]
        for r in self.roles:
            if r in roles:
                return r
        return None

    @property
    def simple_json(self):
        return {
            'id': self.id,
            'showname': self.showname,
            'username': self.username,
        }

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')
        app_label = 'base'

    # 用户扩展信息
    class Exinfo(object):
        def __init__(self, user):
            self.user = user

    @property
    def exinfo(self):
        return User.Exinfo(self)
        # 扩展信息结束


class KeyValue(BaseModel):
    key = models.CharField(_('健'), max_length=255, db_index=True, unique=True)
    type = models.CharField(_('类型'), max_length=255, null=True, blank=True, default="text")
    name = models.CharField(_('名称'), max_length=255, null=True, blank=True)
    value = models.TextField(_('值'), max_length=65535, null=True, blank=True)
    other = models.CharField(_('附加'), max_length=255, null=True, blank=True)

    @classmethod
    def listjson(cls, v):
        if type(v) != list:
            try:
                v = json.loads(v)
            except:
                v = []
        return v

    def get_json(self):
        return {
            'id': self.id,
            'key': self.key,
            'type': self.type,
            'name': self.name,
            'value': self.value,
            'other': self.other
        }

    showitem = {
        'showfield': [
            utils.gen_show_field('键', 'key', 'text'),
            utils.gen_show_field('类型', 'type', 'text'),
            utils.gen_show_field('名称', 'name', 'text'),
            utils.gen_show_field('值', 'value', 'text'),
            utils.gen_show_field('附加', 'other', 'text')
        ],
        'verbose_name': '键值'
    }

    edititem = [
        {'showname': '键', 'name': 'key', 'type': 'text'},
        {'showname': '类型', 'name': 'type', 'type': 'text'},
        {'showname': '名称', 'name': 'name', 'type': 'text'},
        {'showname': '值', 'name': 'value', 'type': 'text'},
        {'showname': '附加', 'name': 'other', 'type': 'text'}
    ]

    @classmethod
    def trystr(cls, v):
        try:
            return str(v)
        except:
            pass
        return unicode(v)

    TYPE_MAP = {
        'text': lambda s: KeyValue.trystr(s) if s else "",
        'largetext': lambda s: KeyValue.trystr(s) if s else "",
        'int': lambda s: int(s) if s else 0,
        'float': lambda s: float(s) if s else 0.0,
        'bool': lambda s: s and s.upper() == "TRUE",
        'imagelinks': lambda s: KeyValue.listjson(s),
        'texts': lambda s: [v.strip() for v in s.split(';') if v.strip()],
        'keyvals': lambda s: KeyValue.listjson(s),
    }

    def __unicode__(self):
        return u'%s(%s)' % (self.name, self.key)

    class Meta:
        verbose_name = _('设置')
        verbose_name_plural = _('设置')
        ordering = ['ordering']
        app_label = 'base'

    @property
    def pyvalue(self):
        return KeyValue.TYPE_MAP[self.type](self.value) if self.type in KeyValue.TYPE_MAP else None

    @classmethod
    def gen_setting(cls, dft=None, ckord=False):
        '''def=[(key,type,name,value,other)]'''
        kvs = dict((v[0], v) for v in dft) if dft else None
        ks = [v[0] for v in dft] if dft else None
        query = KeyValue.objects
        if ks:
            query = query.filter(key__in=ks)
        res = {}
        items = [i for i in query]
        for i in items:
            if ks and i.key in ks:
                ks.remove(i.key)
            res[i.key] = i.pyvalue
        if ks:
            arr = []
            for k in ks:
                v = kvs[k]
                kv = KeyValue(key=k, type=v[1], name=v[2], value=v[3], other=v[4])
                arr.append(kv)
                res[k] = kv.pyvalue
            KeyValue.objects.bulk_create(arr)
        if ckord and dft:
            ks = [v[0] for v in dft]
            idic = dict([(i.key, i) for i in KeyValue.objects.filter(key__in=ks)])
            for ordering, di in enumerate(dft):
                key = di[0]
                if key in idic:
                    item = idic[key]
                    other = di[4]
                    name = di[2]
                    stype = di[1]
                    if item.ordering != ordering or item.other != other or item.name != name or item.type != stype:
                        item.ordering = ordering
                        item.other = other
                        item.name = name
                        item.type = stype
                        item.save()
        return res


class ActionLog(BaseModel):
    user = models.ForeignKey(to=User, verbose_name=_('用户'), null=True, blank=True)
    action = models.CharField(_('动作'), null=True, blank=True, max_length=255)
    content = models.TextField(_('内容'), null=True, blank=True)
    model = models.CharField(_('模型'), null=True, blank=True, max_length=64)
    objsid = models.CharField(_('对象IDs'), null=True, blank=True, max_length=255)
    model_cn = models.CharField(_('中文件模型名称'), null=True, blank=True, max_length=255)

    ACTION_CREATE = 'create'
    ACTION_MODIFY = 'modify'
    ACTION_DELETE = '删除'
    ACTION_LOCK = 'lock'
    ACTION_LOGIN = '登录'
    ACTION_REGISTER = 'register'
    ACTION_CLEAN = 'clean'
    ACTION_ADD = '添加'
    ACTION_EDIT = '编辑'

    @property
    def showname(self):
        return u'%s %s %s(%s) %s' % (self.user, self.action, self.model_cn, self.model, self.objsid)

    def get_json(self):
        content = self.content
        objsid = self.objsid
        print self.content
        if utils.is_json_list(self.content) and self.content != '' and self.content:
            content = '<br>'.join(json.loads(self.content))
        if ',' in self.objsid:
            objsid = '<br>'.join(str(self.objsid).split(','))
        return {
            'user': None,
            'id': self.id,
            'user_text': self.user.showname,
            'action': self.action,
            'content': content,
            'model': self.model,
            'objsid': objsid,
            'model_cn': self.model_cn,
            'model_text': (self.model_cn if self.model_cn else '') + '-' + (self.model if self.model else ''),
            'created_text': self.created.strftime("%Y-%m-%d %H:%M:%S"),
            'ordering': self.ordering
        }

    showitem = {
        'showfield': [
            utils.gen_show_field('用户', 'user_text', config.SHOW_TEXT),
            utils.gen_show_field('动作', 'action', config.SHOW_TEXT),
            utils.gen_show_field('模型', 'model_text', config.SHOW_TEXT),
            utils.gen_show_field('内容', 'content', config.SHOW_HTML),
            # utils.gen_show_field('对象ids','objsid',config.SHOW_HTML),
            utils.gen_show_field('时间', 'created_text', config.SHOW_HTML)
        ]
    }

    class Meta:
        verbose_name = _('日志')
        verbose_name_plural = _('日志')
        app_label = 'base'

    def __unicode__(self):
        return self.showname
