# -*- coding: UTF-8 -*
'''
Copyright 2016 INRUAN Technology Co., Ltd. All rights reserved.

Created on 2016-01-31

@author: Robin
'''

import time

import xlwt
from django.conf.urls import patterns
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt

import siteinfo
from bapi import BaseApiView
from base import utils, config
from base.models import User
from base.utils import ex, gen_query_json, gen_query_json_list_array
from base.views import asapi
from info.models import ClassCourseInfo, EnrollCourseInfo, ClassInfo
from qbsy import settings
from student.models import TaskRecord, Task

unlogin = asapi(logined=False)  # 无需登录的API
logined = asapi(logined=True)  # 需要登录的API
admin = asapi(logined=True, userrole='admin')  # 管理员
teacher = asapi(logined=True, userrole=['admin', 'teacher'])
student = asapi(logined=True, userrole=['admin', 'teacher', 'student'])
admin_and_reception = asapi(logined=True, userrole=['admin', 'reception', 'super_reception'])


class ApiView(BaseApiView):
    @property
    def get_host(self):
        return 'http://' + self.request.get_host() + '/api/'

    @logined
    def getUserList(self, _param):
        """
        获取用户列表
        @param _param: 
        @return: 
        """
        from base.models import Role
        query = User.objects.filter()
        if 'role' in _param:
            roleids = [r.id for r in Role.objects.filter(role=_param['role'])]
            if roleids:
                query = query.filter(role_id__in=roleids)
        return gen_query_json_list_array(query, _param)

    @logined
    def get_select_model_list(self, modelname, querydic=None):
        """
        获取模型选择列表
        @param modelname: 
        @return: 
        """
        model = self.getModel(modelname)
        query = model.objects.filter().order_by('-ordering', '-id') if not querydic else model.objects.filter(
            **querydic).order_by('-ordering', '-id')
        data = [m.get_select_json() for m in query] if hasattr(model, 'get_select_json') else [m.get_json() for m in
                                                                                               query]
        return data

    @unlogin
    def get_model_search_key(self, modelname):
        from config import searchkeyconfig
        return searchkeyconfig.get(modelname, None)

    def gen_edit_item(self, model, _param):
        edititem = model.edititem
        for item in edititem:
            if item['type'] == 'select':
                if item.get('isforeignkey'):
                    querydic = item.get('querydic', None)
                    defaultselect_q = item.get('defaultselect_q')
                    if not querydic and defaultselect_q and _param.get(defaultselect_q):
                        querydic = {'id': _param.get(defaultselect_q)}
                    item['default'] = self.get_select_model_list(item['name'], querydic=querydic) if not item.get(
                        'modelname', None) else self.get_select_model_list(item['modelname'], querydic=querydic)
            if item['type'] == 'rolecheckbox':
                if hasattr(siteinfo, 'site_' + item['name']):
                    item['default'] = getattr(siteinfo, 'site_' + item['name'])
            if item['type'] == 'select_2':
                if item.get('isforeignkey'):
                    querydic = item.get('querydic', None)
                    item['default'] = self.get_select_model_list(item['name'], querydic=querydic) if not item.get(
                        'select_one_modelname', None) else self.get_select_model_list(item['select_one_modelname'],
                                                                                      querydic=querydic)
                    item['default_2'] = self.get_select_model_list(item.get('select_two_modelname'))
            if item.get('type') == 'modelconfig':
                from modelinfo import get_app_models
                item['default'] = [m.__name__ for m in get_app_models()]
        return edititem

    @logined
    def get_model_editfiled(self, modelname, _param):
        """
        获取模型选择字段
        @param modelname: 
        @return: 
        """
        model = self.getModel(modelname)
        if not self.check_permission(modelname, 'is_edit'):
            raise ex(u'用户权限不足')
        if self.check_permission(modelname, 'is_self'):
            self.verify_user(None, None, _param, is_edit=True)
        if hasattr(model, 'edititem'):
            return {'edititem': self.gen_edit_item(model, _param)}
        else:
            raise ex('%s没有设置edititem属性' % modelname)

    @logined
    def get_model_viewfield(self, modelname, _param):
        """
        获取模型的查看字段
        :param modelname:
        :param _param:
        :return:
        """
        model = self.getModel(modelname)
        if not self.check_permission(modelname, 'is_view'):
            raise ex(u'用户权限不足')
        if self.check_permission(modelname, 'is_self'):
            self.verify_user(None, None, _param, is_edit=True)
        if hasattr(model, 'edititem'):
            return {'edititem': self.gen_edit_item(model, _param)}
        else:
            raise ex('%s没有设置edititem属性' % modelname)

    @logined
    def getModelData(self, modelname, id, _param):
        """
        获取模型数据，仅一个
        @param modelname: 
        @param id: 
        @param _param: 
        @return: 
        """
        model = self.getModel(modelname)
        if not self.check_permission(modelname, 'is_view'):
            raise ex(u'用户权限不足')
        query = model.objects.filter()
        if self.check_permission(modelname, 'is_self'):
            if self.get_me().isteacher:
                query = self.verify_user(query, config.model_self_teacher.get(modelname), _param)
            if self.get_me().isstudent:
                query = self.verify_user(query, config.model_self_student.get(modelname), _param)
        query = query.filter(id=id)
        if query is not None:
            if hasattr(model, 'get_json'):
                return gen_query_json(query, param=_param)
            else:
                raise ex('%s没有get_json()方法' % modelname)
        else:
            raise ex(u'无法查询到数据')

    @logined
    def get_model_data_v2(self, modelname, _param):
        """
        获取单个模型数据第二个版本
        :param modelname:
        :param _param:
        :return:
        """
        model = self.getModel(modelname)
        if not self.check_permission(modelname, 'is_view'):
            raise ex(u'用户权限不足')
        query = model.objects.filter()
        if self.check_permission(modelname, 'is_self'):
            if self.get_me().isteacher:
                query = self.verify_user(query, config.model_self_teacher.get(modelname), _param)
            if self.get_me().isstudent:
                query = self.verify_user(query, config.model_self_student.get(modelname), _param)
        query = query.filter()
        if query is not None:
            if hasattr(model, 'get_json'):
                return gen_query_json(query, param=_param)
            else:
                raise ex('%s没有get_json()方法' % modelname)
        else:
            raise ex(u'无法查询到数据')

    @admin
    def get_user_data(self, id):
        """
        获取某个用户数据
        @param id:
        @return:
        """
        from base.models import User
        u = User.objects.filter(id=id).first()
        return u.get_json()

    @unlogin
    def upload_file(self):
        """
        上传文件
        @type:post
        @param file:文件，格式为:js:form.append('file', file);
        @return: 文件上传后返回:{'url':文件的相对路径, 'filename': 文件名,'size':文件大小,'img_info':图片信息(如果是图片，支持jpg,png,gif)}
        @return: img_info:{'normal_info': 原始图片信息, 'small_info': 小图信息,'middle_info': 中图信息)}
        @return: normal_info:{'url': 图片相对路径链接, 'size': 文件大小, 'width': 图片宽, 'height': 图片高}
        """
        import time, os, datetime
        import utils
        if self.request.method == "POST":
            file = self.request.FILES.get("file", None)
            filename = str(int(round(time.time() * 1000))) + '.' + file.name.split('.')[-1]
            filetype = file.name.split('.')[-1]
            upload_root = 'media/upload'
            now = datetime.datetime.now()
            uplaod_path = upload_root + '/' + str(now.year) + str(now.month)
            if not os.path.exists(uplaod_path):
                os.mkdir(uplaod_path)
            filepath = os.path.join(uplaod_path, filename)
            f = open(filepath, 'wb')
            for chunk in file.chunks():
                f.write(chunk)
            f.close()
            res = {'url': '/' + filepath, 'filename': file.name, 'size': os.path.getsize(filepath)}
            if filetype == 'png' or filetype == 'jpg' or filetype == 'gif':
                res['img_info'] = utils.get_full_compress_img_info(filepath)
            return res
        else:
            raise ex('请使用post方法上传')

    @unlogin
    def upload_files(self):
        """
        多文件上传
        @type:post
        @param files:文件，格式为:form.append(files[i].name, files[i]);
        @return: 返回为文件列表，信息与单个文件的一样
        """
        import time, os, datetime
        import utils
        file_url_list = []
        if self.request.method == "POST":
            upload_root = 'media/upload'
            now = datetime.datetime.now()
            uplaod_path = os.path.join(upload_root, str(now.year) + str(now.month))
            if not os.path.exists(uplaod_path):
                os.mkdir(uplaod_path)
            for filename in self.request.FILES:
                file = self.request.FILES.get(filename, None)
                filename_h = str(int(round(time.time() * 1000))) + '.' + file.name.split('.')[-1]
                filepath = os.path.join(uplaod_path, filename_h)
                filetype = file.name.split('.')[-1]
                f = open(filepath, 'wb')
                for chunk in file.chunks():
                    f.write(chunk)
                f.close()
                item = {'url': '/' + filepath, 'filename': file.name, 'size': os.path.getsize(filepath)}
                if filetype == 'png' or filetype == 'jpg' or filetype == 'gif':
                    item['img_info'] = utils.get_full_compress_img_info(filepath)
                file_url_list.append(item)
            return file_url_list
        else:
            raise ex('请使用post方法上传')

    def write_to_temp(self, file, dirpath):
        import time, os
        filename = file.name.split('.')[0] + '_' + str(int(time.time())) + '.' + file.name.split('.')[-1]
        f = open(os.path.join(dirpath, filename), 'wb')
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        return dirpath + '/' + filename

    @logined
    def get_setting(self, keys):
        """
        获取设置信息
        @param keys: 
        @return: 
        """
        from base.models import KeyValue
        from base.siteinfo import site_setting
        settings = None
        if keys:
            settings = keys.split(',')
        site_settings = [s[0] for s in site_setting]
        if settings:
            site_settings = [ss for ss in site_settings if ss in settings]
        return [kv.get_json() for kv in KeyValue.objects.filter() if kv.get_json()['key'] in site_settings]

    @logined
    def get_setting_dic(self):
        """
        获取设置的字典
        @return: 
        """
        from models import KeyValue
        setting_dic = {}
        for k in [kv.get_json() for kv in KeyValue.objects.filter()]:
            setting_dic[k['key']] = k['value']
        return setting_dic

    @logined
    def export_to_excel(self, modelname, _param):
        model = self.getModel(modelname)
        if not self.check_permission(modelname, 'is_export'):
            raise ex(u'用户权限不足')
        _param['size'] = -1
        _param['page'] = 1
        data = self.getModelList(modelname, _param)
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('sheet1')
        datalist = data.items
        if hasattr(model, 'exportlist'):
            exportlist = model.exportlist
            for index, el in enumerate(exportlist):
                worksheet.write(0, index, el['showname'])
            for index, dl in enumerate(datalist):
                for index_j, el in enumerate(exportlist):
                    worksheet.write(index + 1, index_j, dl[el['fieldname']])
            timestrap = str(int(time.time()))
            path = settings.BASE_DIR + '/media/temp/' + 'export_' + timestrap + '.xls'
            workbook.save(path)
            return '/media/temp/' + 'export_' + timestrap + '.xls'
        else:
            raise ex('导出条目没有配置')

    @teacher
    def get_teacher_course_list(self, _param):
        """
        获取老师的课程列表
        :param teacherid: 
        :return: 
        """
        query = ClassCourseInfo.objects.filter()
        query = self.verify_user(query, 'teacherinfo_id', _param)
        return utils.gen_query_json_list_array(query, _param, funcstr='get_course_json', funcdic={})

    @student
    def get_student_course_list(self, studentid, _param):
        """
        获取学生的课程列表
        :param studentid: 
        :return: 
        """
        query = ClassCourseInfo.objects.filter(enrollcourseinfo__enrollinfo__user_id=studentid)
        return utils.gen_query_json_list_array(query, _param, funcstr='get_course_json', funcdic={})

    @teacher
    def get_course_task_list(self, courseid, _param):
        """
        通过课程的id得到作业的列表
        :param courseid: 
        :param _param: 
        :return: 
        """
        query = Task.objects.filter(course_id=courseid)
        return utils.gen_query_json_list_array(query, _param)

    @student
    def get_teacher_info(self, teacherid):
        """
        获取老师信息
        :param teacherid: 
        :return: 
        """
        query = User.objects.filter(id=teacherid).first()
        return utils.gen_query_json(query)

    @teacher
    def get_task_record_list(self, taskid, _param):
        """
        得到作业记录列表
        :param taskid: 
        :return: 
        """
        query = TaskRecord.objects.filter(task_id=taskid)
        query = self.verify_user(query, 'task__course__teacherinfo_id', _param)
        return utils.gen_query_json_list_array(query, _param)

    @student
    def get_student_task_list(self, courseid, userid, _param):
        """
        获取学生的作业记录列表
        :param taskid: 
        :param userid: 
        :param _param: 
        :return: 
        """
        query = Task.objects.filter(course_id=courseid)
        return utils.gen_query_json_list_array(query, _param, None, 'get_student_score_json', {'userid': userid})

    @teacher
    def get_teacher_student_list(self, courseid, _param):
        """
        通过课程的id得到学生列表
        :param courseid: 
        :param _params: 
        :return: 
        """
        query = EnrollCourseInfo.objects.filter(gradecourseinfo_id=courseid)
        query = self.verify_user(query, 'gradecourseinfo__teacherinfo_id', _param)
        return utils.gen_query_json_list_array(query, _param, funcstr='get_teacher_json', funcdic={})

    @teacher
    def export_course_excel(self, _param):
        query = ClassCourseInfo.objects.filter()
        query = self.verify_user(query, 'teacherinfo_id', _param)
        listfields = ['courseinfo_name', 'classinfo_name', 'coursestarttime_text', 'courseendtime_text', 'coursetime',
                      'coursecount', 'studentcount', 'taskcount', 'preenrollcount', 'coursestatus']
        data = utils.gen_query_json_list_array(query, _param, listfields=listfields, funcstr='get_course_json',
                                               funcdic={})
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('sheet1')
        datalist = data.items
        export_header = ('课程名', '班级', '课程开始时间', '课程结束时间', '上课时间', '课时', '学生数', '作业数', '学生预报名数', '课程状态')
        for index, el in enumerate(export_header):
            worksheet.write(0, index, el)
        for index, dl in enumerate(datalist):
            for index_j, el in enumerate(listfields):
                worksheet.write(index + 1, index_j, dl[el])
        timestrap = str(int(time.time()))
        path = settings.BASE_DIR + '/media/temp/' + 'export_' + timestrap + '.xls'
        workbook.save(path)
        return '/media/temp/' + 'export_' + timestrap + '.xls'

    @teacher
    def export_task_scores_excel(self, courseid, _param):
        ecis = EnrollCourseInfo.objects.filter(gradecourseinfo_id=courseid)
        student_ids = [eci.enrollinfo.user.id for eci in ecis]
        students = User.objects.filter(id__in=student_ids)
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('sheet1')
        export_header = ['学生姓名'] + [t.taskname for t in Task.objects.filter(course_id=courseid)]
        for index, el in enumerate(export_header):
            worksheet.write(0, index, el)
        for index, stu in enumerate(students):
            print stu.showname
            for index_j, el in enumerate(TaskRecord.objects.filter(user=stu, task__course_id=courseid)):
                print el.score
                if index_j == 0:
                    worksheet.write(index + 1, index_j, stu.showname)
                    worksheet.write(index + 1, index_j + 1, el.score)
                else:
                    worksheet.write(index + 1, index_j + 1, el.score)
        timestrap = str(int(time.time()))
        path = settings.BASE_DIR + '/media/temp/' + 'export_' + timestrap + '.xls'
        workbook.save(path)
        return '/media/temp/' + 'export_' + timestrap + '.xls'

    @logined
    def export_course_task(self, courseid):
        from base_v2.utils_v2 import write_list_to_excel
        import uuid
        query = TaskRecord.objects.filter(task__course_id=courseid)
        excel_item = []
        excel_item.append(['课程', '作业', '学生', '分值', '评语'])
        for q in query:
            excel_item.append([q.task.course.showname, q.task.taskname, q.user.showname, q.score, q.feedback])
        return write_list_to_excel(excel_item, uuid.uuid4().hex + '.xls')

    @admin_and_reception
    def get_model_stat(self, modelname, nameparam, valueparam, title, subtitle, _param, is_set=None, showname=None,
                       modelname_two=None):
        """
        得到模型统计
        :param _param:
        :return:
        """
        model = self.getModel(modelname)
        param_dic = utils.get_queryfilters(_param)
        query = None
        if is_set and int(is_set) == 1:
            ids = list(set([q.id for q in model.objects.filter(**param_dic)]))
            query = model.objects.filter(pk__in=ids).values(nameparam).annotate(value=Count(valueparam))
        else:
            query = model.objects.filter(**param_dic).values(nameparam).annotate(value=Count(valueparam))
        query_list = []
        for q in query:
            q_dic = {}
            for k in q:
                if k != 'value':
                    q_dic['name'] = q[k]
                else:
                    q_dic[k] = q[k]
            query_list.append(q_dic)
        if showname and str(showname != '') and modelname_two:
            for q in query_list:
                q['name'] = getattr(self.getModel(modelname_two).objects.filter(id=q['name']).first(),
                                    showname if showname != '1' else 'showname')
        return {'items': query_list, 'title': title, 'subtitle': subtitle,
                'legenddata': [q['name'] for q in query_list]}

    def get_stat_split_list(self, split_string):
        return [(s if s != '-1' else None) for s in str(split_string).split(',')]

    @admin_and_reception
    def get_model_stats(self, modelnames, nameparams, valueparams, titles, subtitles, querys, is_sets, shownames,
                        modelname_twos):
        data_list = []
        modelname_list = self.get_stat_split_list(modelnames)
        nameparam_list = self.get_stat_split_list(nameparams)
        valueparam_list = self.get_stat_split_list(valueparams)
        title_list = self.get_stat_split_list(titles)
        subtitle_list = self.get_stat_split_list(subtitles)
        query_list = self.get_stat_split_list(querys)
        is_set_list = self.get_stat_split_list(is_sets)
        showname_list = self.get_stat_split_list(shownames)
        modelname_two_list = self.get_stat_split_list(shownames)
        for index, m in enumerate(modelname_list):
            data_list.append(self.get_model_stat(m, nameparam_list[index], valueparam_list[index], title_list[index],
                                                 subtitle_list[index], query_list[index], is_set_list[index],
                                                 showname_list[index], modelname_two_list[index]))
        return data_list

    @admin_and_reception
    def get_class_doing(self):
        """
        得到当前正在进行的课程群列表
        :return: 
        """
        query = ClassInfo.objects.filter()
        json_list = []
        for q in query:
            if q.is_doing():
                json_list.append(q.get_classinfo_json())
        return utils.gen_json_list_array(json_list, size=-1)

    @admin_and_reception
    def get_class_data(self, modelname, id):
        """
        得到当前正在进行的课程群列表
        :return:
        """
        query = ClassInfo.objects.filter(pk=id)
        query1 = ClassInfo.objects.filter(pk=id).first()
        return utils.gen_query_json(query, param=None, extra_dic=query1.get_classinfo_json())


urlpatterns = patterns('',
                       (r'(?P<apiname>\S+)', csrf_exempt(ApiView.as_view())),
                       )
