# -*- coding: UTF-8 -*-
import json

from base import config
from base.models import ActionLog, User
from base.utils import dic2obj, obj2dic, ex, gen_pager_array, splitstrip, gen_query_json_list_array
from base.views import ApiView, asapi
import utils

unlogin = asapi(logined=False)  # 无需登录的API
logined = asapi(logined=True)  # 需要登录的API
admin = asapi(userrole='admin')  # 管理员

admin_and_reception = asapi(logined=True, userrole=['admin', 'reception'])


class BaseApiView(ApiView):
    def verify_user(self, query, queryfield, _param, is_edit=False):
        user_id = _param.get('s_user_id') or _param.get('user_id')
        if not user_id or self.get_me().id != int(user_id):
            raise ex('访问受限')
        if is_edit:
            return True
        querydic = {queryfield: user_id}
        query = query.filter(**querydic)
        return query

    def getIds(self, ids):
        if type(ids) != list:
            ids = [i.strip() for i in ids.split(',') if i.strip()]
        return ids

    def logAtion(self, action, model=None, objsid=None, content=None, model_cn=None):
        '''记录日志'''
        if not self.site.setting.get('logable'):
            return
        if not objsid:
            objsid = ''
        if type(objsid) in [list, tuple, set]:
            objsid = ','.join('%s' % i for i in objsid)
        else:
            objsid = u'%s' % objsid
        if type(content) == list:
            content = json.dumps(content)
        print content
        log = ActionLog(action=action, model=model.__name__ if model else None, objsid=objsid, content=content,
                        model_cn=model_cn)
        meid = self.get_meid()
        if meid:
            log.user_id = meid
        log.save()

    @unlogin
    def login(self, username, password):
        """
        用户登录
        @param username: 
        @param password: 
        @return: 
        """
        user = User.objects.filter(username=username).first()
        if user and user.password == User.pwdhash(password, user.salt):
            if user.status == User.STATUS_CANCELED:
                raise ex(u'该用户已被锁定无法登陆')
            self.session_set('me', user.get_json())
            self.logAtion(ActionLog.ACTION_LOGIN)
            logingoto = self.session_get_once('logingoto')
            return obj2dic(user, ['id', 'username', 'token'], {
                'goto': logingoto or '/xadmin/'
            })
        else:
            raise ex(u'用户名或密码错误')

    @unlogin
    def logout(self):
        """
        退出登录
        @return: 
        """
        self.session_del('me')

    @logined
    def saveUserInfo(self, _param):
        '''
        保存个人信息
        @param _param: 
        @return: 
        '''
        utils.verify_phone_format(_param.get('phone', ''))
        me = self.get_me()
        dic2obj(me, ['phone', 'truename', 'address', 'icon', 'style'], _param)
        me.save()

    @logined
    def changePassword(self, password, newpassword):
        '''
        修改用户密码
        @param password: 
        @param newpassword: 
        @return: 
        '''
        if not newpassword:
            raise ex(u'新密码不能为空')
        user = self.get_me()
        if user and user.password == User.pwdhash(password, user.salt):
            user.password = User.pwdhash(newpassword, user.salt)
            user.save()
        else:
            raise ex(u'原密码不正确!')

    @logined
    def changeUserInfo(self, _param):
        '''
        修改用户密码
        @param _param: 
        @return: 
        '''
        user = self.get_me()
        dic2obj(user, ['name', 'email', 'phone', 'address', 'icon', 'language', 'style'], _param)
        user.save()

    def getModel(self, modelname):
        model = ApiView.getModel(self, modelname)
        if not model:
            raise ex(u'不存在模型:%s' % modelname)
        return model

    @logined
    def getModelList(self, modelname, _param):
        '''
        获取模型对于的数据列表
        @param modelname: 
        @param _param: 
        @return: 
        '''
        model = self.getModel(modelname)
        if not self.check_permission(modelname, 'is_view'):
            raise ex(u'用户权限不足')
        query = model.objects.filter()
        if self.check_permission(modelname, 'is_self'):
            if self.get_me().isteacher:
                query = self.verify_user(query, config.model_self_teacher.get(modelname), _param)
            if self.get_me().isstudent:
                query = self.verify_user(query, config.model_self_student.get(modelname), _param)
            if self.get_me().is_teacher_assistant:
                query = self.verify_user(query, config.model_self_teacher_assistant.get(modelname), _param)
        if hasattr(model, 'get_list_json'):
            if hasattr(model, 'showitem'):
                shwoitem = model.showitem if not hasattr(model.showitem, '__call__') else model.showitem()
                return gen_query_json_list_array(query, param=_param, showitem=shwoitem, funcstr='get_list_json',
                                                 funcdic={})
        if hasattr(model, 'get_json'):
            if hasattr(model, 'showitem'):
                shwoitem = model.showitem if not hasattr(model.showitem, '__call__') else model.showitem()
                return gen_query_json_list_array(query, param=_param, showitem=shwoitem)
            return gen_query_json_list_array(query, param=_param)
        else:
            raise ex('%s没有get_json()方法' % modelname)

    @logined
    def saveModel(self, modelname, _param):
        '''
        保存模型数据
        @param modelname: 
        @param _param: 
        @return: 
        '''
        is_add = False
        if not self.check_permission(modelname, 'is_edit'):
            raise ex(u'用户权限不足')
        model = self.getModel(modelname)
        # if hasattr(model, 'role_write') and not self.get_me().checkrole(model.role_write):
        #     raise ex(u'用户权限不足:%s' % model.role_write)
        objid = _param.get('id')
        o = model.objects.filter(pk=objid).first()
        if o:
            if modelname == 'User' and _param.get('password', None) == '':
                _param.pop('password')
        else:
            is_add = True
            if modelname == 'User':
                print _param.get('username', None)
                u = User.objects.filter(username=_param.get('username', None))
                if u:
                    raise ex('该用户已经存在')
            o = model()
        emptyfields = []
        fields = model.get_editfields()
        for f in model.get_fields():
            if f.name in fields and (not f.blank and not f.null) and not _param.get(f.name, None):
                if hasattr(f, 'rel') and hasattr(f.rel, 'to'):
                    fn = f.name + "_id" if not f.name.endswith('_id') else f.name
                    if not _param.get(fn, None):
                        emptyfields.append(f.verbose_name)
                else:
                    emptyfields.append(f.verbose_name)
                    if modelname == 'User' and f.name == 'password' and not is_add:
                        emptyfields.pop()
            if (
                    f.__class__.__name__ == 'ForeignKey' or f.__class__.__name__ == 'OneToOneField') and not f.name.endswith(
                '_id') and hasattr(f, 'rel') and f.editable and not f.primary_key and hasattr(f.rel, 'to'):
                fields.remove(f.name)
                fields.append(f.name + "_id")
                if _param.get(f.name + '_id') == '':
                    _param[f.name + '_id'] = None
            if f.__class__.__name__ == 'ChildrenModelField' and f.name in fields:
                fields.remove(f.name)
            if (f.__class__.__name__ == 'DateField' or f.__class__.__name__ == 'IntegerField' or f.__class__.__name__=='FloatField') and _param.get(
                    f.name) == '':
                _param[f.name] = None
        if emptyfields:
            efs = ','.join(emptyfields).decode('utf-8')
            raise ex(u"'%s'不能为空" % (efs))
        if hasattr(o, 'modify'):
            o.modify(self.get_me(), fields, _param)
        else:
            dic2obj(o, fields, _param)

        if self.check_permission(modelname, 'is_self'):
            self.verify_user(None, None, _param, is_edit=True)
        o.save()
        if is_add:
            self.logAtion(ActionLog.ACTION_ADD, model=model,
                          content=o.__unicode__() if hasattr(o, '__unicode__') else None, objsid=o.id,
                          model_cn=o._meta.verbose_name)
            print o._meta.verbose_name
        else:
            self.logAtion(ActionLog.ACTION_EDIT, model=model,
                          content=o.__unicode__() if hasattr(o, '__unicode__') else None, objsid=o.id,
                          model_cn=o._meta.verbose_name)
        return o.get_json()

    def delModelsByIds(self, model, ids):
        '''
        批量删除模型数据
        @param model: 
        @param ids: 
        @return: 
        '''
        # if hasattr(model, 'role_write') and not self.get_me().checkrole(model.role_write):
        #     raise ex(u'用户权限不足:%s' % model.role_write)
        ids = self.getIds(ids)
        delete_content = []
        if ids:
            delete_content = [(m.__unicode__() if hasattr(m, '__unicode__') else None) for m in
                              model.objects.filter(pk__in=ids)]
            model.objects.filter(pk__in=ids).delete()
            if hasattr(model(), 'main'):
                model.raw_objects.filter(main_id__in=ids).delete()
        self.logAtion(ActionLog.ACTION_DELETE, model, ids, content=delete_content, model_cn=model._meta.verbose_name)
        return len(ids)

    @logined
    def delModels(self, modelname, ids):
        '''
        删除模型数据
        @param modelname: 
        @param ids: 
        @return: 
        '''
        # if not self.check_opration(modelname):
        #     raise ex(u'用户权限不足')
        # if self.get_me().isreception:
        #     raise ex(u'用户权限不足，请联系管理员进行操作')
        # if (self.get_me().isstudent or self.get_me().isteacher) and (modelname=='Exam'):
        #     raise ex(u'用户权限不足')
        if not self.check_permission(modelname, 'is_delete'):
            raise ex(u'用户权限不足')
        ids = ids.split(',')
        model = self.getModel(modelname)
        return self.delModelsByIds(model, ids)

    @admin_and_reception
    def topModels(self, modelname, ids):
        '''
        置顶模型
        @param modelname: 
        @param ids: 
        @return: 
        '''
        if not self.check_permission(modelname, 'is_top'):
            raise ex(u'用户权限不足')
        ids = ids.split(',')
        model = self.getModel(modelname)
        if ids:
            from utils import orderinggen
            ordering = orderinggen()
            ix = 0
            for o in model.objects.filter(pk__in=ids):
                o.ordering = ordering - ix
                o.save()
                ix += 1
        return len(ids)

    @logined
    def cancel_top(self, modelname, ids):
        """
        取消置顶
        :param modelname: 
        :param ids: 
        :return: 
        """
        if not self.check_permission(modelname, 'is_top'):
            raise ex(u'用户权限不足')
        ids = ids.split(',')
        model = self.getModel(modelname)
        if ids:
            for o in model.objects.filter(pk__in=ids):
                o.ordering = 0
                o.save()
        return len(ids)

    def setUsersStatus(self, modelname, ids, status):
        '''
        取消计划
        @param modelname: 
        @param ids: 
        @param status: 
        @return: 
        '''
        model = self.getModel(modelname)
        ids = ids.split(',')
        if '1' in ids:
            ids.remove('1')
        if ids:
            model.objects.filter(pk__in=ids).update(status=status)
        return len(ids)

    @admin
    def cancelUsers(self, modelname, ids):
        """
        锁定用户
        @param modelname: 
        @param ids: 
        @return: 
        """
        return self.setUsersStatus(modelname, ids, User.STATUS_CANCELED)

    @admin
    def backUsers(self, modelname, ids):
        """
        激活用户
        @param modelname: 
        @param ids: 
        @return: 
        """
        return self.setUsersStatus(modelname, ids, User.STATUS_NORMAL)

    @admin
    def delUsers(self, ids):
        """
        删除用户
        @param ids: 
        @return: 
        """
        ids = ids.split(',')
        if '1' in ids:
            ids.remove('1')
        if ids:
            from info.models import Student
            for id in ids:
                Student.objects.filter(user_id=id).delete()
            User.objects.filter(pk__in=ids).delete()
        self.logAtion(ActionLog.ACTION_DELETE, User, ids)
        return len(ids)

    @admin
    def saveUser(self, _param):
        """
        保存用户信息
        @param _param: 
        @return: 
        """
        flag_add = True
        user = User.objects.filter(pk=_param['id']).first() if _param.get('id', None) else None
        if user:
            flag_add = False
        if user and User.objects.exclude(pk=_param['id']).filter(username=_param['username']).count():
            raise ex(u'该用户名已经存在!')
        if not user:
            if _param.get('username', None) and User.objects.filter(username=_param['username']):
                raise ex(u'该用户名已经存在!')
            user = User()
        dic2obj(user, ['username', 'truename', 'name', 'email', 'phone', 'department_id', 'role_id'], _param)
        if _param.get('password', ''):
            user.password = _param['password']
        user.save()
        self.logAtion(ActionLog.ACTION_MODIFY, User, user.id)

    @admin
    def getLogList(self, _param):
        '''
        获取日志列表
        @param _param: 
        @return: 
        '''
        query = ActionLog.objects.select_related('user').order_by('-id')
        fields = ['id', 'action', 'model', 'objsid', 'created']
        return gen_pager_array(query, func=lambda o: obj2dic(o, fields, {'user': o.user.showname if o.user else None}),
                               param=_param)

    @admin
    def delLogs(self, ids=''):
        '''
        删除日志
        @param ids: 
        @return: 
        '''
        ids = self.getIds(ids)
        if ids:
            ActionLog.objects.filter(pk__in=ids).delete()
            self.logAtion(ActionLog.ACTION_DELETE, ActionLog, ids)
        else:
            ActionLog.objects.filter().delete()
            self.logAtion(ActionLog.ACTION_CLEAN, ActionLog)

    @logined
    def saveSetting(self, _param):
        '''
        保存设置
        @param _param: 
        @return: 
        '''
        if not self.check_permission('KeyValue', 'is_edit'):
            raise ex(u'用户权限不足')
        ks = [k for k in _param if not k.startswith('_')]
        resks = []
        if ks:
            from base.models import KeyValue
            for kv in KeyValue.objects.filter(key__in=ks):
                k = kv.key
                kv.value = _param[k]
                try:
                    kv.pyvalue
                    kv.save()
                    resks.append(k)
                except:
                    print 'saveSetting of key %s' % kv.key
                    pass
            from siteinfo import Site
            Site.reset()
        return resks

    @logined
    def changeUserByRole(self, roleid):
        '''
        根据角色切换用户,开发阶段使用
        @param roleid: 
        @return: 
        '''
        if self.site.setting.get('sys_debug'):
            user = User.objects.filter(role_id=roleid, status=User.STATUS_NORMAL).first()
            if not user:
                raise ex(u'没有该角色用户')
            self.logout()
            self.session_set('me', user.get_json())
        else:
            raise ex(u'该功能已经禁用')

    @logined
    def changeUser(self, userid):
        '''
        切换用户,开发阶段使用
        @param userid: 
        @return: 
        '''
        if self.site.setting.get('sys_debug'):
            user = User.objects.filter(pk=userid).first()
            if not user:
                raise ex(u'没有该角色用户')
            self.logout()
            self.session_set('me', user.get_json())
        else:
            raise ex(u'该功能已经禁用')
