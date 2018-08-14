# -*- coding: UTF-8 -*-
import time

from base import config, modelinfo
from models import CallMixin

site_setting = [
    # 网站信息
    ('sitename', 'text', u'网站名称', '', None),
    ('address', 'text', u'地址', '', None),
    ('zip', 'text', u'邮编', '', None),
    ('copyright', 'text', 'copyright', '', None),
    # SEO
    ('keywords', 'text', u'关键字', '', None),
    ('description', 'largetext', u'网站描述', '', None),
    # 信息设置
    ('sys_debug', 'bool', u'系统调试', 'false', None),
    ('logable', 'bool', u'日志记录', 'false', None),
    ('staticversion', 'text', u'静态资源版本', '', None),
    ('sys_notice', 'largetext', u'系统公告', '', None)
]


def gen_opration(key, name, value=None, isedit=True, isshow=True, href=None, isme=False, isadd=True, is_delete=True):
    return {
        'k': key,
        'name': name,
        'value': value,
        'isedit': isedit,
        'isshow': isshow,
        'href': href,
        'isme': isme,
        'isadd': isadd,
        'isdelete': is_delete
    }


opration_k = [
    ('xuser_mgr', 2), ('xuser_role_mgr', 3), ('sys_seo_setting', 8), ('sys_base_setting', 9),
    ('sys_site_setting', 10), ('xuser_admin_mgr', 11), ('xuser_teacher_mgr', 12), ('xuser_student_mgr', 13),
    ('xuser_reception_mgr', 14), ('studentinfo_mgr', 15), ('school_mgr', 16), ('grade_mgr', 17),
    ('year_mgr', 18), ('course_mgr', 19), ('payee_mgr', 20), ('courseclass_mgr', 21), ('olddata_mgr', 22),
    ('enrollinfo_mgr', 23), ('allcourse_mgr', 24), ('teacherinfo_mgr', 25), ('dropcourse_mgr', 26),
    ('preenrollinfo_mgr', 27), ('task_mgr', 28), ('tasksubject_mgr', 29), ('taskrecord_mgr', 30),
    ('teacher_config', 31), ('student_config', 32), ('log_mgr', 33), ('sys_setting_system_notice', 34),
    ('xuser_super_reception_mgr', 35), ('xuser_teacher_assistant_mgr', 36)
]

opration_k_map = dict(opration_k)

site_oprations = [
    {
        'name': '基础信息管理', 'icon': '&#xe70f;',
        'oprations': [
            gen_opration(opration_k_map.get('school_mgr'), '学校管理', 'SchoolInfo', isedit=True,
                         href='/xadmin/modellist.html?modelname=SchoolInfo'),
            gen_opration(opration_k_map.get('grade_mgr'), '年级届次管理', 'GradeInfo', isedit=True,
                         href='/xadmin/modellist.html?modelname=GradeInfo'),
            gen_opration(opration_k_map.get('year_mgr'), '学年管理', 'SchoolYearInfo', isedit=True,
                         href='/xadmin/modellist.html?modelname=SchoolYearInfo'),
            gen_opration(opration_k_map.get('course_mgr'), '课程管理', 'CourseInfo', isedit=True,
                         href='/xadmin/modellist.html?modelname=CourseInfo'),
        ]
    },
    {
        'name': '学生信息管理', 'icon': '&#xe611;',
        'oprations': [
            gen_opration(opration_k_map.get('studentinfo_mgr'), '学生信息',
                         'User,EnrollInfo,EnrollCourseInfo,EnrollCourseLeaveInfo,Exam',
                         href='/xadmin/modellist.html?modelname=User&q__role__id=3', isedit=True),
            gen_opration(opration_k_map.get('enrollinfo_mgr'), '协议列表', 'EnrollInfo',
                         href='/xadmin/modellist.html?modelname=EnrollInfo', isedit=True, isadd=False),
            gen_opration(opration_k_map.get('preenrollinfo_mgr'), '预报名信息', 'PreEnrollInfo',
                         href='/xadmin/modellist.html?modelname=PreEnrollInfo', isedit=True),
            gen_opration(opration_k_map.get('olddata_mgr'), '历史数据管理', 'OldData', isedit=True,
                         href='/xadmin/modellist.html?modelname=OldData'),
        ]
    },
    {
        'name': '教师信息管理', 'icon': '&#xe62d;',
        'oprations': [
            gen_opration(opration_k_map.get('teacherinfo_mgr'), '教师信息', 'User',
                         href='/xadmin/modellist.html?modelname=User&q__role__id=2', isedit=True),
            gen_opration(opration_k_map.get('xuser_teacher_assistant_mgr'), '教辅信息', 'User',
                         href='/xadmin/modellist.html?modelname=User&q__role__id=6', isedit=True),
        ]
    },
    {
        'name': '课程信息管理', 'icon': '&#xe720;',
        'oprations': [
            gen_opration(opration_k_map.get('courseclass_mgr'), '课程群管理', 'ClassInfo,ClassCourseInfo', isedit=True,
                         href='/xadmin/modellist.html?modelname=ClassInfo'),
            gen_opration(opration_k_map.get('allcourse_mgr'), '所有课程', 'ClassCourseInfo,TaskSubject,Task',
                         isedit=True,
                         href='/xadmin/modellist.html?modelname=ClassCourseInfo', isadd=False),
        ]
    },
    {
        'name': '用户信息管理', 'icon': '&#xe62b;',
        'oprations': [
            gen_opration(opration_k_map.get('xuser_admin_mgr'), '管理员用户', 'User',
                         href='/xadmin/modellist.html?modelname=User&q__role__id=1', isedit=True),
            gen_opration(opration_k_map.get('xuser_teacher_mgr'), '老师用户', 'User',
                         href='/xadmin/modellist.html?modelname=User&q__role__id=2', isedit=True),
            gen_opration(opration_k_map.get('xuser_student_mgr'), '学生用户', 'User',
                         href='/xadmin/modellist.html?modelname=User&q__role__id=3', isedit=True),
            gen_opration(opration_k_map.get('xuser_reception_mgr'), '行政用户', 'User',
                         href='/xadmin/modellist.html?modelname=User&q__role__id=4', isedit=True),
            gen_opration(opration_k_map.get('xuser_super_reception_mgr'), '行政主管用户', 'User',
                         href='/xadmin/modellist.html?modelname=User&q__role__id=5', isedit=True),
            gen_opration(opration_k_map.get('xuser_teacher_assistant_mgr'), '教辅用户', 'User',
                         href='/xadmin/modellist.html?modelname=User&q__role__id=6', isedit=True),
        ]
    },
    {
        'indexname': '系统设置', 'icon': '&#xe61d;', 'name': '系统设置',
        'oprations': [
            gen_opration(opration_k_map.get('sys_seo_setting'), 'seo设置', 'KeyValue', isedit=False, isshow=True,
                         href='/xadmin/kvsetting.html?keys=keywords,description'),
            gen_opration(opration_k_map.get('sys_site_setting'), '网站信息设置', 'KeyValue', isedit=False, isshow=True,
                         href='/xadmin/kvsetting.html?keys=sitename,address,zip,copyright'),
            gen_opration(opration_k_map.get('log_mgr'), '查看日志', 'ActionLog', isedit=False, isshow=True,
                         href='/xadmin/modellist.html?modelname=ActionLog&isadd=-1&isdelete=-1&isedit=-1'),
            gen_opration(opration_k_map.get('sys_setting_system_notice'), '系统公告', 'KeyValue', isedit=False, isshow=True,
                         href='/xadmin/kvsetting.html?keys=sys_notice'),
        ]
    },
]


class Site(object, CallMixin):
    '''模板注入静态对象'''
    autotemplage = True
    easyversion = u'-1.4.4'

    @property
    def timestamp(self):
        import time
        return int(time.time())

    _setting = None

    def get_site_oprations(self):
        return site_oprations

    @classmethod
    def reset(cls):
        Site._setting = None

    @property
    def setting(self):
        # 设置
        from models import KeyValue
        if not Site._setting:
            Site._setting = KeyValue.gen_setting(site_setting, ckord=True)
        return Site._setting

    def get_setting(self):
        from models import KeyValue
        setting_dic = {}
        for k in [kv.get_json() for kv in KeyValue.objects.filter()]:
            setting_dic[k['key']] = k['value']
        return setting_dic

    def getModel(self, modelname):
        return modelinfo.getModel(modelname=modelname)

    template_engines = {}

    def get_objs(self, modelname, count=0):
        model = self.getModel(modelname)
        if model:
            if int(count):
                return model.objects.filter()[0:count]
            else:
                return model.objects.filter()
        else:
            raise Exception("no model of %s" % modelname)

    def get_objs_orderby(self, modelname, orderby, count=0):
        model = self.getModel(modelname)
        if model:
            return model.objects.order_by('-' + str(orderby))[0:count]
        else:
            raise Exception("no model of %s" % modelname)

    @property
    def roles(self):
        from base.models import Role
        return Role.objects.filter()


gsite = Site()


def get_gsite():
    global gsite
    return gsite
