# -*- coding: UTF-8 -*
import json

import time
from django.db import models
from pypinyin import lazy_pinyin
from base.models import BaseModel, _, User
from base import utils, config, filedutils


class NewsBase(BaseModel):
    title = models.CharField(_('标题'), max_length=255, db_index=True)
    abstract = models.TextField(_('摘要'), null=True, blank=True)
    picture = models.TextField(_('标题图片'), null=True, blank=True)
    content = models.TextField(_('内容'), null=True, blank=True)

    def get_json(self):
        return {
            'abstract': self.abstract,
            'content': self.content,
            'id': self.id,
            'title': self.title,
            'picture': self.picture,
            'created': self.created.strftime("%Y-%m-%d %H:%I:%S")
        }

    showitem = {
        'showfield': [
            utils.gen_show_field('标题', 'title', 'text'),
            utils.gen_show_field('图片', 'picture', 'img'),
            utils.gen_show_field('更新时间', 'created', 'text'),
        ],
        'verbose_name': '新闻'
    }

    edititem = [
        utils.gen_edit_field('标题', 'title', 'text', verify='required', helptext='请输入标题'),
        utils.gen_edit_field('摘要', 'abstract', 'textarea', verify='required'),
        utils.gen_edit_field('标题图片', 'picture', 'img'),
        utils.gen_edit_field('内容', 'content', 'kingeditor')
    ]

    def __unicode__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name = _('新闻')
        verbose_name_plural = _('新闻')
        app_label = 'info'


class News(NewsBase):
    showitem = {
        'showfield': [
            utils.gen_show_field('标题', 'title', 'text'),
            utils.gen_show_field('图片', 'picture', 'img'),
            utils.gen_show_field('更新时间', 'created', 'text'),
        ],
        'verbose_name': '新闻'
    }

    class Meta:
        verbose_name = _('新闻')
        verbose_name_plural = _('新闻')
        app_label = 'info'


class Notice(NewsBase):
    showitem = {
        'showfield': [
            utils.gen_show_field('标题', 'title', 'text'),
            utils.gen_show_field('图片', 'picture', 'img'),
            utils.gen_show_field('更新时间', 'created', 'text'),
        ],
        'verbose_name': '通知公告'
    }

    def __unicode__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name = _('通知公告')
        verbose_name_plural = _('通知公告')
        app_label = 'info'


class Research(NewsBase):
    showitem = {
        'showfield': [
            utils.gen_show_field('标题', 'title', 'text'),
            utils.gen_show_field('图片', 'picture', 'img'),
            utils.gen_show_field('更新时间', 'created', 'text'),
        ],
        'verbose_name': '科研活动'
    }

    def __unicode__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name = _('科研活动')
        verbose_name_plural = _('科研活动')
        app_label = 'info'


class Cover(BaseModel):
    title = models.CharField(_('标题'), max_length=255, db_index=True)
    img = models.TextField(_('图片'))
    link = models.TextField(_('链接'), null=True)

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'img': self.img,
            'link': self.link
        }

    showitem = {
        'showfield': [
            utils.gen_show_field('标题', 'title', 'text'),
            utils.gen_show_field('图片', 'img', 'img'),
            utils.gen_show_field('图片链接', 'link', 'text'),
        ],
        'verbose_name': '封面流'
    }

    edititem = [
        utils.gen_edit_field('标题', 'title', 'text', verify='required', helptext='请输入标题'),
        utils.gen_edit_field('图片', 'img', 'img'),
        utils.gen_edit_field('链接', 'link', 'text', helptext='请输入有效的url链接')
    ]

    def __unicode__(self):
        return '%s' % (self.title)

    class Meta:
        verbose_name = _('封面流')
        verbose_name_plural = _('封面流')
        app_label = 'info'


class SchoolInfo(BaseModel):
    """
    学校表
    """
    schoolname = models.CharField(verbose_name='学校名称', max_length=255, db_index=True)
    schooldesc = models.TextField(verbose_name='学校描述', blank=True, null=True)

    @property
    def showname(self):
        return self.schoolname

    def get_json(self):
        return {
            'id': self.id,
            'name': self.schoolname,
            'schoolname': self.schoolname,
            'schooldesc': self.schooldesc,
            'ordering': self.ordering
        }

    showitem = {
        'showfield': [
            utils.gen_show_field('学校名称', 'schoolname', 'text'),
            utils.gen_show_field('学校描述', 'schooldesc', 'text')
        ],
        'verbose_name': '学校信息',
        'isexport': True
    }

    edititem = [
        utils.gen_edit_field('学校名称', 'schoolname', 'text', verify='required', helptext='输入学校名称'),
        utils.gen_edit_field('学校描述', 'schooldesc', 'textarea', helptext='输入学校的大致描述，可为空')
    ]

    exportlist = [
        utils.gen_export_field('学校名称', 'schoolname'),
        utils.gen_export_field('学校描述', 'schooldesc')
    ]

    def __unicode__(self):
        return self.schoolname

    class Meta:
        app_label = 'info'
        verbose_name = '学校信息'
        verbose_name_plural = '学校信息'


class GradeInfo(BaseModel):
    """
    年级届次表
    """
    gradename = models.CharField(verbose_name='年级名称', max_length=255, db_index=True)
    gradedesc = models.TextField(verbose_name='年级描述', blank=True, null=True)

    @property
    def showname(self):
        return self.gradename

    def get_json(self):
        return {
            'id': self.id,
            'name': self.gradename,
            'gradename': self.gradename,
            'gradedesc': self.gradedesc,
            'ordering': self.ordering
        }

    showitem = {
        'showfield': [
            utils.gen_show_field('年级信息', 'gradename', 'text'),
            utils.gen_show_field('年级描述', 'gradedesc', 'text')
        ],
        'verbose_name': '年级届次信息',
        'isexport': True
    }

    edititem = [
        utils.gen_edit_field('年级名称', 'gradename', 'text', verify='required', helptext='输入年级名称，如2017届'),
        utils.gen_edit_field('年级描述', 'gradedesc', 'textarea', helptext='输入年级的大致描述，可为空')
    ]

    exportlist = [
        utils.gen_export_field('年级名称', 'gradename'),
        utils.gen_export_field('年级描述', 'gradedesc')
    ]

    def __unicode__(self):
        return self.gradename

    class Meta:
        app_label = 'info'
        verbose_name = '年级信息'
        verbose_name_plural = '年级信息'


class SchoolYearInfo(BaseModel):
    """
    学年信息管理
    """
    schoolyearname = models.CharField(verbose_name='学年名称', max_length=255, db_index=True)
    schoolyeardesc = models.TextField(verbose_name='学年信息描述', blank=True, null=True)

    @property
    def showname(self):
        return self.schoolyearname

    def get_json(self):
        return {
            'id': self.id,
            'schoolyearname': self.schoolyearname,
            'schoolyeardesc': self.schoolyeardesc,
            'name': self.schoolyearname,
            'ordering': self.ordering
        }

    showitem = {
        'showfield': [
            utils.gen_show_field('学年名称', 'schoolyearname', 'text'),
            utils.gen_show_field('学年信息描述', 'schoolyeardesc', 'text')
        ],
        'verbose_name': '学年信息',
        'isexport': True
    }

    edititem = [
        utils.gen_edit_field('学年名称', 'schoolyearname', 'text', verify='required', helptext='学年名称，如2017年'),
        utils.gen_edit_field('学年信息描述', 'schoolyeardesc', 'textarea', helptext='学年信息描述')
    ]

    exportlist = [
        utils.gen_export_field('学年名称', 'schoolyearname'),
        utils.gen_export_field('学年信息描述', 'schoolyeardesc')
    ]

    def __unicode__(self):
        return self.schoolyearname

    class Meta:
        app_label = 'info'
        verbose_name = '学年信息'
        verbose_name_plural = '学年信息'


class ClassInfo(BaseModel):
    """
    课程群信息
    """
    schoolyearinfo = models.ForeignKey(verbose_name='学年信息', to=SchoolYearInfo, null=True, blank=True,
                                       on_delete=models.SET_NULL)
    classname = models.CharField(verbose_name='课程群类型', max_length=255, db_index=True)
    starttime = models.DateField(verbose_name='课程群开始时间', null=True, blank=True)
    endtime = models.DateField(verbose_name='课程群结束时间', null=True, blank=True)
    classdesc = models.TextField(verbose_name='课程群类型描述', null=True, blank=True)

    @property
    def showname(self):
        return (self.schoolyearinfo.schoolyearname if self.schoolyearinfo else '') + '-' + self.classname

    @property
    def is_course_doing(self):
        query = ClassCourseInfo.objects.filter(classinfo=self)
        for q in query:
            if q.is_doing:
                return True
        return False

    def is_doing(self):
        now = time.time()
        if self.starttime and self.endtime:
            starttime = time.mktime(self.starttime.timetuple())
            endtime = time.mktime(self.endtime.timetuple())
            return now > starttime and now < endtime
        else:
            return False

    @property
    def get_course_count(self):
        return ClassCourseInfo.objects.filter(classinfo=self).count()

    @property
    def get_coure_status(self):
        cci = ClassCourseInfo.objects.filter(classinfo=self)
        coursestatus_ids = []
        for cc in cci:
            coursestatus_ids.append(cc.get_coursestatus_id)
        return {
            'status_0': coursestatus_ids.count(0),
            'status_1': coursestatus_ids.count(1),
            'status_2': coursestatus_ids.count(2),
            'status_3': coursestatus_ids.count(3),
            'status_4': coursestatus_ids.count(4)
        }

    @property
    def get_student_count(self):
        query = ClassCourseInfo.objects.filter(classinfo=self)
        return User.objects.filter(enrollinfo__enrollcourseinfo__gradecourseinfo__in=query).distinct().count()

    @property
    def get_preenroll_count(self):
        return PreEnrollInfo.objects.filter(course__classinfo=self).count()

    def get_json(self):
        ecis = EnrollCourseInfo.objects.filter(gradecourseinfo__classinfo=self)
        student_count = ecis.count()
        course_doing_count = ecis.filter(status=0).count()
        course_leaving_count = ecis.filter(status=2).count()
        course_willdoing_count = ecis.filter(status=1).count()
        leaving_rate = '%.2f%%' % (
            (float(course_leaving_count) / float(student_count)) * 100.0 if student_count != 0 else 0.0)
        return {
            'ordering': self.ordering,
            'student_count_true': self.get_student_count,
            'starttime': self.starttime,
            'starttime_text': utils.get_datefiled_text(self.starttime),
            'endtime': self.endtime,
            'endtime_text': utils.get_datefiled_text(self.endtime),
            'leaving_rate': leaving_rate,
            'course_doing_count': course_doing_count,
            'course_will_doing_count': course_willdoing_count,
            'course_leaving_count': course_leaving_count,
            'student_count': student_count,
            'preenroll_count': self.get_preenroll_count,
            'id': self.id,
            'name': self.schoolyearinfo.schoolyearname + '-' + self.classname,
            'classname': self.classname,
            'classdesc': self.classdesc,
            'schoolyearinfo_id': utils.get_foreignkey_value(self.schoolyearinfo, 'id'),
            'schoolyearinfo_name': utils.get_foreignkey_value(self.schoolyearinfo, 'schoolyearname'),
            'view_course_link': "B.addWindowTab('管理" + self.showname + "课程信息','/xadmin/modellist.html?modelname=ClassCourseInfo&q__classinfo_id=" + str(
                self.id) + "')",
            'view_stat': "B.addWindowTab('查看" + self.showname + "统计','/xadmin/model_statistics_normal.html?modelname=User&q__enrollinfo__enrollcourseinfo__gradecourseinfo__classinfo__id=" + str(
                self.id) + "&nameparam=school__schoolname&valueparam=school&is_set=1&title=" + self.showname + "&subtitle=为学生生源比例,非课程人次')",
        }

    def get_classinfo_json(self):
        res = self.get_json()
        res['course_count'] = self.get_course_count
        res.update(self.get_coure_status)
        return res

    showitem = {
        'showfield': [
            utils.gen_show_field('学年名称', 'schoolyearinfo_name', 'text'),
            utils.gen_show_field('课程群名称', 'classname', 'text'),
            utils.gen_show_field('课程群开始时间', 'starttime_text', 'text'),
            utils.gen_show_field('课程群结束时间', 'endtime_text', 'text'),
            utils.gen_show_field('预报名人次', 'preenroll_count', 'text'),
            utils.gen_show_field('实际学生人数', 'student_count_true', 'text'),
            utils.gen_show_field('总人次', 'student_count', 'text'),
            utils.gen_show_field('上课人次', 'course_doing_count', 'text'),
            utils.gen_show_field('保留课时人次', 'course_will_doing_count', 'text'),
            utils.gen_show_field('退课人次', 'course_leaving_count', 'text'),
            utils.gen_show_field('退课率', 'leaving_rate', 'text')
        ],
        'verbose_name': '课程群类型',
        'linkfield': [
            utils.gen_link_field(None, '<span style="color:gray;">&nbsp;|&nbsp;</span>', islink=False),
            utils.gen_link_field('view_course_link', '查看课程'),
            utils.gen_link_field('view_stat', '查看统计')
        ],
        'isexport': True
    }

    edititem = [
        utils.gen_edit_field('学年', 'schoolyearinfo', 'select', verify='required', helptext='选择学年'),
        utils.gen_edit_field('课程群名称', 'classname', 'text', verify='required', helptext='输入课程群类型名称，如春季班'),
        utils.gen_edit_field('课程群开始时间', 'starttime', config.EDIT_LAYDATE, helptext='请选择课程群开始时间'),
        utils.gen_edit_field('课程群结束时间', 'endtime', config.EDIT_LAYDATE, helptext='请选择课程群结束时间'),
        utils.gen_edit_field('课程群类型描述', 'classdesc', 'textarea', helptext='输入该课程群类型的大致描述')
    ]

    exportlist = [
        utils.gen_export_field('学年', 'schoolyearinfo_name'),
        utils.gen_export_field('课程群名称', 'classname'),
        utils.gen_export_field('开始时间', 'starttime_text'),
        utils.gen_export_field('结束时间', 'endtime_text'),
        utils.gen_export_field('课程群类型描述', 'classdesc'),
        utils.gen_export_field('预报名人数', 'preenroll_count'),
        utils.gen_export_field('学生数', 'student_count'),
        utils.gen_export_field('上课人数', 'course_doing_count'),
        utils.gen_export_field('退课人数', 'course_leaving_count'),
        utils.gen_export_field('退课率', 'leaving_rate')
    ]

    def __unicode__(self):
        return self.schoolyearinfo.schoolyearname + ' ' + self.classname

    class Meta:
        app_label = 'info'
        verbose_name = '课程群类型'
        verbose_name_plural = '课程群类型信息'


class CourseInfo(BaseModel):
    """
    课程信息
    """
    coursename = models.CharField(verbose_name='课程名称', max_length=255, db_index=True)
    coursedesc = models.TextField(verbose_name='课程描述', blank=True, null=True)

    @property
    def showname(self):
        return self.coursename

    def get_json(self):
        return {
            'ordering': self.ordering,
            'id': self.id,
            'coursename': self.coursename,
            'name': self.coursename,
            'coursedesc': self.coursedesc
        }

    edititem = [
        utils.gen_edit_field('课程名称', 'coursename', type='text', verify='required', helptext='输入课程名称，如文数'),
        utils.gen_edit_field('课程描述', 'coursedesc', type='textarea', helptext='输入该课程的大致描述'),
    ]

    showitem = {
        'showfield': [
            utils.gen_show_field('课程名称', 'coursename', type='text'),
            utils.gen_show_field('课程描述', 'coursedesc', type='text')
        ],
        'verbose_name': '课程信息',
        'isexport': True
    }

    exportlist = [
        utils.gen_export_field('课程名称', 'coursename'),
        utils.gen_export_field('课程描述', 'coursedesc')
    ]

    def __unicode__(self):
        return self.coursename

    class Meta:
        app_label = 'info'
        verbose_name = '课程信息'
        verbose_name_plural = '课程信息'


class ClassCourseInfo(BaseModel):
    """
    课程群课程信息
    """
    coursestatus_choice = [[0, '未开始'], [1, '进行中'], [2, '已结课'], [3, '未开班'], [4, '已停课']]
    coursestatus_choice_map = dict(coursestatus_choice)

    # 其它的课程状态

    classinfo = models.ForeignKey(verbose_name='课程群信息', to=ClassInfo, null=True, blank=True, on_delete=models.SET_NULL)
    gradeinfo = models.ForeignKey(verbose_name='年级或届次', to=GradeInfo, null=True, blank=True, on_delete=models.SET_NULL)
    teacherinfo = models.ForeignKey(verbose_name='老师信息', to=User, null=True, blank=True, on_delete=models.SET_NULL)
    courseinfo = models.ForeignKey(verbose_name='课程', to=CourseInfo, null=True, blank=True, on_delete=models.SET_NULL)
    courseclassname = models.CharField(verbose_name='班级名称', max_length=255, blank=True, null=True)
    coursestarttime = models.DateField(verbose_name='课程开始时间')
    courseendtime = models.DateField(verbose_name='课程结束时间')
    coursecount = models.IntegerField(verbose_name='课时')
    coursetime = models.TextField(verbose_name='上课时间', null=True, blank=True)

    extrastatus = models.IntegerField(verbose_name='课程开班状态', choices=coursestatus_choice[2:], null=True, blank=True)
    extrastatusreason = models.TextField(verbose_name='开班状态原因', null=True, blank=True)
    coursedesc = models.TextField(verbose_name='课程描述', null=True, blank=True)
    coursenotice = models.TextField(verbose_name='课程公告', null=True, blank=True)

    @property
    def showname(self):
        return (self.classinfo.schoolyearinfo.showname if self.classinfo else '') \
               + '-' + (self.classinfo.classname if self.classinfo else '') + \
               '-' + (self.gradeinfo.showname if self.gradeinfo else '') + '-' \
               + (self.teacherinfo.showname if self.teacherinfo else '') + \
               '-' + (self.courseinfo.coursename if self.courseinfo else '') + \
               '-' + (self.courseclassname if self.courseclassname else '')

    @property
    def showname_front(self):
        return (self.classinfo.schoolyearinfo.showname if self.classinfo else '') \
               + '-' + (self.classinfo.classname if self.classinfo else '') + \
               '-' + (self.gradeinfo.showname if self.gradeinfo else '') + \
               '-' + (self.courseinfo.coursename if self.courseinfo else '')

    @property
    def showname_two(self):
        return (self.gradeinfo.showname if self.gradeinfo else '') + '-' \
               + (self.teacherinfo.showname if self.teacherinfo else '') + \
               '-' + (self.courseinfo.coursename if self.courseinfo else '') + \
               '-' + (self.courseclassname if self.courseclassname else '')

    @property
    def showname_stat(self):
        return (self.gradeinfo.showname if self.gradeinfo else '') + '-' \
               + (self.teacherinfo.showname if self.teacherinfo else '') + \
               '-' + (self.courseinfo.coursename if self.courseinfo else '') + \
               '-' + (self.courseclassname if self.courseclassname else '')

    @property
    def is_doing(self):
        now = time.time()
        starttime = time.mktime(self.coursestarttime.timetuple())
        endtime = time.mktime(self.courseendtime.timetuple())
        return now > starttime and now < endtime

    @property
    def get_preenroll_count(self):
        return PreEnrollInfo.objects.filter(course=self).count()

    @property
    def get_coursestatus_id(self):
        coursestatus_id = None
        if not isinstance(self.courseendtime, unicode) and not isinstance(self.coursestarttime, unicode):
            now = time.time()
            starttime = time.mktime(self.coursestarttime.timetuple())
            endtime = time.mktime(self.courseendtime.timetuple())
            if now < starttime:
                coursestatus_id = 0
            if now > starttime and now < endtime:
                coursestatus_id = 1
            if now > endtime:
                coursestatus_id = 2
        if self.extrastatus:
            coursestatus_id = self.extrastatus
        return coursestatus_id

    def get_json(self):
        coursetime_split = str(self.coursetime).split('/')
        preenrollcount = PreEnrollInfo.objects.filter(course=self).count()
        ecis = EnrollCourseInfo.objects.filter(gradecourseinfo=self)
        studentcount = ecis.count()
        course_doing_count = ecis.filter(status=0).count()
        course_willdoing_count = ecis.filter(status=1).count()
        course_leaving_count = ecis.filter(status=2).count()
        leaving_rate = '%.2f%%' % (
            (float(course_leaving_count) / float(studentcount)) * 100.0 if studentcount != 0 else 0.0)
        coursestatus_id = self.get_coursestatus_id
        return {
            'ordering': self.ordering,
            'showname_front': self.showname_front,
            'showname_stat': self.showname_stat,
            'leaving_rate': leaving_rate,
            'course_doing_count': course_doing_count,
            'course_leaving_count': course_leaving_count,
            'course_will_doing_count': course_willdoing_count,
            'course_soul': '上课:%d<br>退课:%d<br>保留课时:%d' % (
                course_doing_count, course_leaving_count, course_willdoing_count),
            'id': self.id,
            'name': self.showname,
            'name_two': self.showname_two,
            'classinfo': None,
            'classinfo_name': utils.get_foreignkey_value(self.classinfo, 'showname'),
            'classinfo_id': utils.get_foreignkey_value(self.classinfo, 'id'),
            'gradeinfo': None,
            'gradeinfo_text': utils.get_foreignkey_value(self.gradeinfo, 'gradename'),
            'gradeinfo_id': utils.get_foreignkey_value(self.gradeinfo, 'id'),
            'teacherinfo': None,
            'teacherinfo_name': utils.get_foreignkey_value(self.teacherinfo, 'showname'),
            'teacherinfo_id': utils.get_foreignkey_value(self.teacherinfo, 'id'),
            'courseinfo': None,
            'courseinfo_name': utils.get_foreignkey_value(self.courseinfo, 'coursename'),
            'courseinfo_id': utils.get_foreignkey_value(self.courseinfo, 'id'),
            'coursestarttime': self.coursestarttime,
            'coursestarttime_text': utils.get_datefiled_text(self.coursestarttime),
            'courseendtime': self.courseendtime,
            'courseendtime_text': utils.get_datefiled_text(self.courseendtime),
            'coursecount': self.coursecount,
            'coursetime': self.coursetime,
            'coursetime_html': '<br>'.join(coursetime_split),
            'coursedesc': self.coursedesc,
            'coursenotice': self.coursenotice,
            'courseclassname': self.courseclassname,
            'preenrollinfo_link': "B.addWindowTab('" + self.showname + "预报名信息','/xadmin/modellist.html?modelname=PreEnrollInfo&q__course_id=" + str(
                self.id) + "')",
            'studentinfo_link': "B.addWindowTab('" + self.showname + "学生信息','/xadmin/modellist.html?modelname=EnrollCourseInfo&q__gradecourseinfo_id=" + str(
                self.id) + "')",
            'taskmgr_link': "B.addWindowTab('" + self.showname + "作业管理','/xadmin/modellist.html?modelname=Task&q__course_id=" + str(
                self.id) + "')",
            'course_stat': "B.addWindowTab('{}课程统计','/xadmin/course/course_stat.html?id={}')".format(self.showname,
                                                                                                     self.id),
            'preenrollcount': preenrollcount,
            'studentcount': studentcount,
            'coursestatus': self.coursestatus_choice_map.get(coursestatus_id),
            'coursestatus_id': coursestatus_id,
            'coursestatus_text': self.get_coursestatus(coursestatus_id),
            'countinfo': '预报名数:' + str(preenrollcount) + '<br>总人数:' + str(studentcount),
            'coursestartendtime': '开始:' + utils.get_datefiled_text(
                self.coursestarttime) + '<br>结束:' + utils.get_datefiled_text(self.courseendtime),
            'coursetwo_text': '课程:' + (self.courseinfo.coursename if self.courseinfo else '') + '<br>课程班名称:' + (
                self.courseclassname if self.courseclassname else ''),
            'extrastatus': self.extrastatus,
            'extrastatus_id': self.extrastatus,
            'extrastatus_text': self.coursestatus_choice_map.get(self.extrastatus),
            'extrastatusreason': self.extrastatusreason
        }

    def get_coursestatus(self, coursestatus_id):
        text = self.coursestatus_choice_map.get(coursestatus_id)
        if coursestatus_id == 0:
            return ' <span class="layui-badge layui-bg-orange">{0}</span>'.format(text)
        if coursestatus_id == 1:
            return ' <span class="layui-badge layui-bg-green">{0}</span>'.format(text)
        if coursestatus_id == 2:
            return ' <span class="layui-badge">{0}</span>'.format(text)
        if coursestatus_id == 3:
            return ' <span class="layui-badge layui-bg-orange">{0}</span>'.format(text)
        if coursestatus_id == 4:
            return ' <span class="layui-badge">{0}</span>'.format(text)

    def get_course_json(self):
        from student.models import Task
        res = self.get_json()
        taskcount = Task.objects.filter(course=self).count()
        res['taskcount'] = taskcount
        return res

    showitem = {
        'showfield': [
            utils.gen_show_field('课程信息', 'showname_front', 'text'),
            # utils.gen_show_field('课程群', 'classinfo_name', 'text'),
            # utils.gen_show_field('年级或届次', 'gradeinfo_text', 'text'),
            utils.gen_show_field('老师', 'teacherinfo_name', 'text'),
            utils.gen_show_field('课程班名称', 'courseclassname', config.SHOW_HTML),
            utils.gen_show_field('课程状态', 'coursestatus_text', config.SHOW_HTML),
            # utils.gen_show_field('课程', 'courseinfo_name', 'text'),
            # utils.gen_show_field('课程班名称', 'courseclassname', 'text'),
            # utils.gen_show_field('开始时间', 'coursestarttime_text', 'text'),
            # utils.gen_show_field('结束时间', 'courseendtime_text', 'text'),
            utils.gen_show_field('课时', 'coursecount', 'text'),
            utils.gen_show_field('起止时间', 'coursestartendtime', config.SHOW_HTML),
            utils.gen_show_field('上课时间', 'coursetime_html', config.SHOW_HTML),
            utils.gen_show_field('数量统计', 'countinfo', config.SHOW_HTML),
            # utils.gen_show_field('上课人次', 'course_doing_count', 'text'),
            utils.gen_show_field('课程状态', 'course_soul', 'html'),
            utils.gen_show_field('退课率', 'leaving_rate', 'text')
            # utils.gen_show_field('学生数', 'studentcount', 'text'),
            # utils.gen_show_field('预报名数', 'preenrollcount', 'text')
        ],
        'verbose_name': '课程群课程信息',
        'isexport': True,
        'linkfield': [
            utils.gen_link_field(None, '<span style="color:gray;">&nbsp;|&nbsp;</span>', islink=False),
            utils.gen_link_field('preenrollinfo_link', '预报名信息'),
            utils.gen_link_field(None, '<br>', islink=False),
            utils.gen_link_field('studentinfo_link', '学生信息'),
            utils.gen_link_field('taskmgr_link', '作业管理'),
            utils.gen_link_field('course_stat', '统计')
        ]
    }

    exportlist = [
        utils.gen_export_field('课程班', 'classinfo_name'),
        utils.gen_export_field('年级或届次', 'gradeinfo_text'),
        utils.gen_export_field('老师', 'teacherinfo_name'),
        utils.gen_export_field('课程', 'courseinfo_name'),
        utils.gen_export_field('课程班名称', 'courseclassname'),
        utils.gen_export_field('开始时间', 'coursestarttime_text'),
        utils.gen_export_field('结束时间', 'courseendtime_text'),
        utils.gen_export_field('课时', 'coursecount'),
        utils.gen_export_field('上课时间', 'coursetime'),
        utils.gen_export_field('学生数', 'studentcount'),
        utils.gen_export_field('预报名数', 'preenrollcount'),
        utils.gen_export_field('上课人数', 'course_doing_count'),
        utils.gen_export_field('退课人数', 'course_leaving_count'),
        utils.gen_export_field('退课率', 'leaving_rate')
        # utils.gen_export_field('课程描述', 'coursedesc'),
        # utils.gen_export_field('课程公告', 'coursenotice')
    ]

    edititem = [
        utils.gen_edit_field('课程班', 'classinfo', 'select', verify='required', helptext='选择课程群', disabled=True,
                             defaultselect_q='q__classinfo_id'),
        utils.gen_edit_field('年级或届次', 'gradeinfo', 'select', verify='required', helptext='选择年级或届次',
                             modelname='GradeInfo'),
        utils.gen_edit_field('老师', 'teacherinfo', 'select', verify='required', helptext='请选择老师', modelname='User',
                             querydic={'role__role': 'teacher'}),
        utils.gen_edit_field('课程', 'courseinfo', 'select', verify='required', helptext='选择课程'),
        utils.gen_edit_field('课程班名称', 'courseclassname', 'text', verify=config.VERIFY_REQUIRED,
                             helptext='输入当前课程班的名称，如数学一班'),
        utils.gen_edit_field('开始时间', 'coursestarttime', 'laydate', verify='required', helptext='选择开始时间'),
        utils.gen_edit_field('结束时间', 'courseendtime', 'laydate', verify='required', helptext='选择课程结束时间'),
        utils.gen_edit_field('课时', 'coursecount', 'text', verify='required|int', helptext='输入课时，为一个整数'),
        utils.gen_edit_field('上课时间', 'coursetime', 'textarea', helptext='输入上课时间,使用英文/进行分割'),
        utils.gen_edit_field('开班状态', 'extrastatus', config.EDIT_SELECT, helptext='请选择课程的开班状态,如果是尚未开始的课程，请置空，不要选择',
                             rel_type=config.REL_TYPE_NO_REL_HAS_KEY,
                             isforeignkey=False, default=utils.gen_select_field(dict(coursestatus_choice[3:]))),
        utils.gen_edit_field('开班状态原因', 'extrastatusreason', config.EDIT_TEXTAREA, helptext='记录未开课原因，停课原因，停课时间等信息'),
        utils.gen_edit_field('课程描述', 'coursedesc', 'kingeditor', helptext='输入课程描述'),
        utils.gen_edit_field('课程公告', 'coursenotice', config.EDIT_KINGEDITOR, helptext='输入课程公告')
    ]

    def __unicode__(self):
        return self.classinfo.classname + ' ' + self.teacherinfo.showname + ' ' + self.courseinfo.coursename

    class Meta:
        app_label = 'info'
        verbose_name_plural = '课程班课程信息'
        verbose_name = '课程班课程信息'


class EnrollInfo(BaseModel):
    """
    报名信息表
    """

    user = models.ForeignKey(verbose_name='用户信息', to=User)
    no = models.CharField(verbose_name='协议编号', max_length=255, blank=True, null=True, db_index=True)
    totalcost = models.CharField(verbose_name='总费用', max_length=255, null=True, blank=True)
    discount = models.CharField(verbose_name='折扣', max_length=255, null=True, blank=True)
    realcost = models.CharField(verbose_name='实收费用', max_length=255, null=True, blank=True)
    paytime = models.DateField(verbose_name='付款时间', null=True, blank=True)
    payee = models.ForeignKey(verbose_name='收款人', to=User, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name='payee_user')
    receiptno = models.CharField(verbose_name='收据单号', max_length=255, null=True, blank=True)
    posno = models.CharField(verbose_name='pos单号', max_length=255, null=True, blank=True)
    note = models.TextField(verbose_name='备注', null=True, blank=True)

    @property
    def showname(self):
        return self.user.showname + '-' + self.no

    def get_json(self):
        return {
            'ordering': self.ordering,
            'id': self.id,
            'name': self.showname,
            'user': self.user.get_json(),
            'user_name': self.user.showname,
            'user_id': self.user.id,
            'no': self.no,
            'totalcost': self.totalcost,
            'discount': self.discount,
            'realcost': self.realcost,
            'payee_name': utils.get_foreignkey_value(self.payee, 'showname'),
            'payee_id': utils.get_foreignkey_value(self.payee, 'id'),
            'paytime': self.paytime,
            'paytime_text': utils.get_datefiled_text(self.paytime),
            'receiptno': self.receiptno,
            'posno': self.posno,
            'note': self.note,
        }

    def get_list_json(self):
        res = self.get_base_json()
        res.update({
            'user_name': utils.get_foreignkey_value(self.user, 'showname'),
            'no': self.no,
            'enrollcourseinfo_link': "B.addWindowTab('" + self.showname + "课程信息','/xadmin/modellist.html?modelname=EnrollCourseInfo&q__enrollinfo_id=" + str(
                self.id) + "')",
        })
        return res

    showitem = {
        'showfield': [
            utils.gen_show_field('用户', 'user_name', 'text'),
            utils.gen_show_field('协议编号', 'no', config.SHOW_TEXT)
        ],
        'verbose_name': '协议信息',
        'linkfield': [
            utils.gen_link_field(None, '<span style="color:gray;">&nbsp;|&nbsp;</span>', islink=False),
            utils.gen_link_field('enrollcourseinfo_link', '课程信息')
        ],
        'isexport': True
    }

    edititem = [
        utils.gen_edit_field('用户', 'user', 'select', disabled=True, helptext='用户', defaultselect_q='q__user_id',
                             verify=config.VERIFY_REQUIRED),
        utils.gen_edit_field('协议编号', 'no', 'text', helptext='输入协议编号'),
        utils.gen_edit_field('总费用', 'totalcost', 'text', helptext='输入总费用,为一个数据，整数或是小数', verify='float'),
        utils.gen_edit_field('折扣', 'discount', 'text', helptext='输入折扣，为一个数据，整数或是小数', verify='float'),
        utils.gen_edit_field('实收费用', 'realcost', 'text', helptext='输入实收费用，为一个数据，整数或是小数', verify='float'),
        utils.gen_edit_field('付款时间', 'paytime', config.EDIT_LAYDATE, helptext='选择付款时间'),
        utils.gen_edit_field('收款人', 'payee', 'select', helptext='选择收款人', modelname='User',
                             querydic={'role_id__in': [1, 4]}),
        utils.gen_edit_field('收据单号', 'receiptno', 'text', helptext='输入收据单号'),
        utils.gen_edit_field('pos单号', 'posno', 'text', helptext='输入pos单号'),
        utils.gen_edit_field('备注', 'note', 'textarea', helptext='为该学生添加备注'),
    ]

    exportlist = [
        utils.gen_export_field('用户', 'user_name'),
        utils.gen_export_field('协议编号', 'no'),
        utils.gen_export_field('总费用', 'totalcost'),
        utils.gen_export_field('折扣', 'discount'),
        utils.gen_export_field('实收费用', 'realcost'),
        utils.gen_export_field('付款时间', 'paytime_text'),
        utils.gen_export_field('收款人', 'payee_name'),
        utils.gen_export_field('收据单号', 'receiptno'),
        utils.gen_export_field('pos单号', 'posno'),
        utils.gen_export_field('备注', 'note'),
    ]

    def __unicode__(self):
        return self.user.showname + self.no

    class Meta:
        app_label = 'info'
        verbose_name = '协议信息'
        verbose_name_plural = '协议信息'


class EnrollCourseInfo(BaseModel):
    """
    报名表中的课程信息
    """

    # 上课状态选择
    status_choice = [[0, '上课'], [1, '保留课时'], [2, '退课']]
    status_choice_map = dict(status_choice)

    # 退款状态选择
    isrefund_choice = [[0, '未退款'], [1, '已退款']]
    isrefund_choice_map = dict(isrefund_choice)

    # # 退课状态选择
    # dropcourse_choice = [[0, '无退课'], [1, '有退课']]
    # dropcourse_choice_map = dict(dropcourse_choice)

    enrollinfo = models.ForeignKey(verbose_name='报名表信息', to=EnrollInfo)
    status = models.IntegerField(verbose_name='状态', choices=status_choice)
    gradecourseinfo = models.ForeignKey(verbose_name='报名课程信息', to=ClassCourseInfo, null=True, blank=True,
                                        on_delete=models.SET_NULL)
    coursecount = models.IntegerField(verbose_name='课时数')
    entrytime = models.DateField(verbose_name='进入上课时间', null=True, blank=True)
    realendtime = models.DateField(verbose_name='结束课程时间', null=True, blank=True)
    # 退课信息
    # isdropcourse = models.IntegerField(verbose_name='是否有退课', choices=dropcourse_choice)
    dropcoursetime = models.DateField(verbose_name='退课时间', null=True, blank=True)
    dropcoursenote = models.TextField(verbose_name='退课原因', null=True, blank=True)
    isrefund = models.IntegerField(verbose_name='退款状态', choices=isrefund_choice)
    refundtime = models.DateField(verbose_name='退款时间', null=True, blank=True)
    refundmoney = models.CharField(verbose_name='退款金额', max_length=255, null=True, blank=True)
    refundnote = models.TextField(verbose_name='退款说明', null=True, blank=True)

    @property
    def showname(self):
        return (self.enrollinfo.showname if self.enrollinfo else '') + '-' + (
            self.gradecourseinfo.showname if self.gradecourseinfo else '')

    def __unicode__(self):
        return self.showname

    def get_json(self):
        return {
            'ordering': self.ordering,
            'id': self.id,
            'name': self.showname if self.showname else None,
            'enrollinfo': self.enrollinfo.get_json(),
            'enrollinfo_text': self.enrollinfo.showname,
            'enrollinfo_id': self.enrollinfo_id,
            'gradecourseinfo': utils.get_foreignkey_value(self.gradecourseinfo, 'get_json'),
            'gradecourseinfo_id': utils.get_foreignkey_value(self.gradecourseinfo, 'id'),
            'gradecourseinfo_text': utils.get_foreignkey_value(self.gradecourseinfo, 'showname'),
            'coursecount': self.coursecount,
            'dropcoursenote': self.dropcoursenote,
            # 'isdropcourse': self.isdropcourse,
            # 'isdropcourse_id': self.isdropcourse,
            # 'isdropcourse_text': self.dropcourse_choice_map.get(self.isdropcourse),
            'status_text': self.status_choice_map.get(self.status),
            'status_id': self.status,
            'status': self.status,
            'dropcoursetime': self.dropcoursetime,
            'dropcoursetime_text': utils.get_datefiled_text(self.dropcoursetime),
            'entrytime': self.entrytime,
            'entrytime_text': utils.get_datefiled_text(self.entrytime),
            'realendtime': self.realendtime,
            'realendtime_text': utils.get_datefiled_text(self.realendtime),
            'isrefund': self.isrefund,
            'isrefund_text': self.isrefund_choice_map.get(self.isrefund),
            'isrefund_id': self.isrefund,
            'refundtime': self.refundtime,
            'refundtime_text': utils.get_datefiled_text(self.refundtime),
            'refundmoney': self.refundmoney,
            'refundnote': self.refundnote,
            'enrollcourseleaveinfo_link': "B.addWindowTab('" + self.showname + "请假信息','/xadmin/modellist.html?modelname=EnrollCourseLeaveInfo&q__enrollcourseinfo_id=" + str(
                self.id) + "')",
            'student_course_stat': "B.addWindowTab('{}统计','/xadmin/course/student_course_stat.html?user_id={}&course_id={}')".format(
                self.showname, self.enrollinfo.user_id, self.gradecourseinfo_id),
            'q__classinfo__id': self.gradecourseinfo.classinfo.id if self.gradecourseinfo and self.gradecourseinfo.classinfo else None
        }

    def get_teacher_json(self):
        res = self.get_json()
        res[
            'student_exam_link'] = "B.addWindowTab('查看" + self.enrollinfo.user.showname + "成绩记录','/xadmin/modellist.html?modelname=Exam&isedit=-1&isdelete=-1&isadd=-1&q__examsubject__coursename=" + (
            self.gradecourseinfo.courseinfo.coursename if self.gradecourseinfo and self.gradecourseinfo.courseinfo else '') + "&q__user_id=" + str(
            self.enrollinfo.user.id) + "')",
        return res

    edititem = [
        utils.gen_edit_field('协议', 'enrollinfo', 'select', disabled=True, verify='required', helptext='协议',
                             modelname='EnrollInfo', defaultselect_q='q__enrollinfo_id'),
        utils.gen_edit_field('课程班课程信息', 'gradecourseinfo', config.EDIT_SELECT_2, verify='required',
                             helptext='选择课程班课程信息', select_two_query_filter='q__classinfo__id',
                             modelname='ClassCourseInfo', select_one_text='请选择课程群', select_two_text='请选择课程',
                             select_one_modelname='ClassInfo', select_two_modelname='ClassCourseInfo'),
        utils.gen_edit_field('课时', 'coursecount', 'text', verify='required|int', helptext='输入学生课时'),
        utils.gen_edit_field('进入上课时间', 'entrytime', config.EDIT_LAYDATE, helptext='选择进入上课时间',
                             verify=config.VERIFY_REQUIRED),
        utils.gen_edit_field('结束课程时间', 'realendtime', config.EDIT_LAYDATE, helptext='选择课程结束时间',
                             verify=config.VERIFY_REQUIRED),
        # utils.gen_edit_field('是否有退课', 'isdropcourse', 'select', helptext='选择是否有退课', rel_type='no_rel_has_key',
        #                      default=utils.gen_select_field(dropcourse_choice_map), isforeignkey=False,
        #                      defaultselect=0),
        utils.gen_edit_field('<strong>状态</strong>', 'status', 'select', helptext='选择该学生的上课状态',
                             rel_type='no_rel_has_key',
                             default=utils.gen_select_field(status_choice_map), defaultselect=0, isforeignkey=False,
                             verify='required'),
        utils.gen_edit_field('退课时间', 'dropcoursetime', config.EDIT_LAYDATE, helptext='选择退课时间'),
        utils.gen_edit_field('退课原因', 'dropcoursenote', 'textarea', helptext='输入退课原因'),

        utils.gen_edit_field('是否有退款', 'isrefund', 'select', helptext='选择该学生的退款状态', rel_type='no_rel_has_key',
                             default=utils.gen_select_field(isrefund_choice_map), defaultselect=0, isforeignkey=False),
        utils.gen_edit_field('退款时间', 'refundtime', config.EDIT_LAYDATE, helptext='选择退款时间', ),
        utils.gen_edit_field('退款金额', 'refundmoney', 'text', helptext='输入退款的金额，为一个数据，整数或是小数'),
        utils.gen_edit_field('退款说明', 'refundnote', 'textarea', helptext='输入退款说明'),
    ]

    showitem = {
        'showfield': [
            utils.gen_show_field('协议', 'enrollinfo_text', 'text'),
            utils.gen_show_field('课程班课程', 'gradecourseinfo_text', 'text'),
            utils.gen_show_field('课时', 'coursecount', 'text'),
            # utils.gen_show_field('是否有退课', 'isdropcourse_text', 'text'),
            utils.gen_show_field('是否有退款', 'isrefund_text', 'text'),
            utils.gen_show_field('听课状态', 'status_text', 'text'),
        ],
        'verbose_name': '协议课程',
        # 'selectfield': [
        #     utils.gen_show_select_field('选择听课状态', utils.gen_select_field(status_choice_map), model_q='q__status',
        #                                 selectid='status_select'),
        #     utils.gen_show_select_field('选择退课状态', utils.gen_select_field(dropcourse_choice_map),
        #                                 model_q='q__isdropcourse',
        #                                 selectid='isdropcourse_select')
        # ],
        'isexport': True,
        'linkfield': [
            utils.gen_link_field('enrollcourseleaveinfo_link', '请假信息'),
            utils.gen_link_field('student_course_stat', '统计')
        ]
    }

    exportlist = [
        utils.gen_export_field('协议', 'enrollinfo_text'),
        utils.gen_export_field('状态', 'status_text'),
        utils.gen_export_field('课程班课程信息', 'gradecourseinfo_text'),
        utils.gen_export_field('课时', 'coursecount'),
        utils.gen_export_field('进入上课时间', 'entrytime_text'),
        utils.gen_export_field('结束课程时间', 'realendtime_text'),
        # utils.gen_export_field('是否有退课', 'isdropcourse_text'),
        utils.gen_export_field('退课时间', 'dropcoursetime_text'),
        utils.gen_export_field('退课原因', 'dropcoursenote')
    ]

    class Meta:
        app_label = 'info'
        verbose_name_plural = '报名表课程'
        verbose_name = '报名表课程'


class EnrollCourseLeaveInfo(BaseModel):
    """课程请假表信息"""
    enrollcourseinfo = models.ForeignKey(verbose_name='协议课程', to=EnrollCourseInfo)
    leavereason = models.TextField(verbose_name='原因')
    leavetime = models.DateField(verbose_name='时间')
    courseindex = models.CharField(verbose_name='第几次', null=True, blank=True, max_length=255)

    @property
    def showname(self):
        return self.enrollcourseinfo.showname + '-' + self.courseindex

    def __unicode__(self):
        return self.showname

    def get_json(self):
        return {
            'ordering': self.ordering,
            'id': self.id,
            # 'enrollcourseinfo': utils.get_foreignkey_value(self.enrollcourseinfo, 'get_json'),
            'enrollcourseinfo_id': utils.get_foreignkey_value(self.enrollcourseinfo, 'id'),
            'enrollcourseinfo_text': utils.get_foreignkey_value(self.enrollcourseinfo, 'showname'),
            'leavereason': self.leavereason,
            'leavetime': self.leavetime,
            'leavetime_text': utils.get_datefiled_text(self.leavetime),
            'courseindex': utils.get_datefiled_text(self.courseindex)
        }

    showitem = {
        'showfield': [
            utils.gen_show_field('课程', 'enrollcourseinfo_text', config.SHOW_TEXT),
            utils.gen_show_field('时间', 'leavetime_text', config.SHOW_TEXT),
            utils.gen_show_field('第几次课', 'courseindex', config.SHOW_TEXT),
            utils.gen_show_field('原因', 'leavereason', config.SHOW_TEXT)
        ],
        'verbose_name': '课程请假信息',
        'isexport': True
    }

    edititem = [
        utils.gen_edit_field('课程', 'enrollcourseinfo', config.EDIT_SELECT, disabled=True, verify=config.VERIFY_REQUIRED,
                             helptext='选择课程', modelname='EnrollCourseInfo', defaultselect_q='q__enrollcourseinfo_id'),
        utils.gen_edit_field('请假时间', 'leavetime', config.EDIT_LAYDATE, verify=config.VERIFY_REQUIRED,
                             helptext='选择请假的时间'),
        utils.gen_edit_field('原因', 'leavereason', config.EDIT_TEXTAREA, verify=config.VERIFY_REQUIRED,
                             helptext='请填写请假的原因'),
        utils.gen_edit_field('第几次课', 'courseindex', config.EDIT_TEXT, helptext='请填写第几次课')
    ]

    exportlist = [
        utils.gen_export_field('课程', 'enrollcourseinfo_text'),
        utils.gen_export_field('请假时间', 'leavetime_text'),
        utils.gen_export_field('原因', 'leavereason'),
        utils.gen_export_field('第几次课', 'courseindex')
    ]

    class Meta:
        verbose_name_plural = '课程退课信息'
        verbose_name = '课程退课信息'
        app_label = 'info'


class PreEnrollInfo(BaseModel):
    """预报名信息"""
    isoldstudent_choice = [[1, '是'], [0, '否']]
    isoldstudent_choice_map = dict(isoldstudent_choice)

    # 获取渠道
    getpath_choice = [[0, '微信公众号'], [1, '宣传单'], [2, '朋友推荐']]
    getpath_choice_map = dict(getpath_choice)

    truename = models.CharField(verbose_name='真实姓名', max_length=20)
    preenrollschool = models.ForeignKey(verbose_name='学校', to=SchoolInfo, null=True, blank=True,
                                        on_delete=models.SET_NULL)
    preenrollgrade = models.ForeignKey(verbose_name='年级', to=GradeInfo, null=True, blank=True,
                                       on_delete=models.SET_NULL)
    phone = models.CharField(verbose_name='电话', max_length=100)
    course = models.ForeignKey(verbose_name='预报课程', to=ClassCourseInfo, null=True, blank=True,
                               on_delete=models.SET_NULL)
    preenrolltime = models.DateField(verbose_name='预报名时间')
    isoldstudent = models.IntegerField(verbose_name='是否是老学员')
    getpath = models.TextField(verbose_name='从哪里获得的信息')
    note = models.TextField(verbose_name='备注', null=True, blank=True)

    @property
    def showname(self):
        return self.truename + '预报名信息'

    def __unicode__(self):
        return self.showname

    def get_json(self):
        getpath_list = json.loads(self.getpath)
        getpath_list_text = ','.join([self.getpath_choice_map.get(int(gl)) for gl in getpath_list])
        username = ''.join(lazy_pinyin(self.truename)) + str(self.phone)[-4:]
        user = User.objects.filter(username=username).first()
        adduser_link = "B.addWindowTab('新建学生" + "','/xadmin/editmodel.html?modelname=User&q__role__id=3&truename=" + self.truename + "&phone=" + self.phone + "&password=123456&username=" + username + "&q__school__id=" + str(
            self.preenrollschool_id) + "&q__grade__id=" + str(self.preenrollgrade_id) + "')"
        if user:
            adduser_link = "B.addWindowTab('" + user.showname + "用户信息" + "','/xadmin/modellist.html?modelname=User&q__id=" + str(
                user.id) + "&q__role__id=3')"
        return {
            'ordering': self.ordering,
            'id': self.id,
            'name': self.showname,
            'truename': self.truename,
            'preenrollschool': utils.get_foreignkey_value(self.preenrollschool, 'get_json'),
            'preenrollschool_id': utils.get_foreignkey_value(self.preenrollschool, 'id'),
            'preenrollschool_text': utils.get_foreignkey_value(self.preenrollschool, 'showname'),
            'preenrollgrade': utils.get_foreignkey_value(self.preenrollgrade, 'get_json'),
            'preenrollgrade_id': utils.get_foreignkey_value(self.preenrollgrade, 'id'),
            'preenrollgrade_text': utils.get_foreignkey_value(self.preenrollgrade, 'showname'),
            'phone': self.phone,
            'course_id': utils.get_foreignkey_value(self.course, 'id'),
            'course_text': utils.get_foreignkey_value(self.course, 'showname'),
            'preenrolltime': self.preenrolltime,
            'preenrolltime_text': utils.get_datefiled_text(self.preenrolltime),
            'isoldstudent': self.isoldstudent,
            'isoldstudent_id': self.isoldstudent,
            'isoldstudent_export_text': self.isoldstudent_choice_map.get(self.isoldstudent),
            'isoldstudent_text': '<span class="layui-badge layui-bg-blue">是</span>' if self.isoldstudent == 1 else '<span class="layui-badge">否</span>',
            'getpath': self.getpath,
            'getpath_list_text': getpath_list_text,
            'note': self.note,
            'adduserlink': adduser_link,
            'isuser': '<span class="layui-badge layui-bg-blue">是</span>' if user else '<span class="layui-badge">否</span>'
        }

    def get_list_json(self):
        res = self.get_base_json()
        username = ''.join(lazy_pinyin(self.truename)) + str(self.phone)[-4:]
        user = User.objects.filter(username=username).first()
        adduser_link = "B.addWindowTab('新建学生" + "','/xadmin/editmodel.html?modelname=User&q__role__id=3&truename=" + self.truename + "&phone=" + self.phone + "&password=123456&username=" + username + "&q__school__id=" + str(
            self.preenrollschool_id) + "&q__grade__id=" + str(self.preenrollgrade_id) + "')"
        if user:
            adduser_link = "B.addWindowTab('" + user.showname + "用户信息" + "','/xadmin/modellist.html?modelname=User&q__id=" + str(
                user.id) + "&q__role__id=3')"
        res.update({
            'truename': self.truename,
            'preenrollschool_text': utils.get_foreignkey_value(self.preenrollschool, 'showname'),
            'preenrollgrade_text': utils.get_foreignkey_value(self.preenrollgrade, 'showname'),
            'phone': self.phone,
            'course_text': utils.get_foreignkey_value(self.course, 'showname'),
            'preenrolltime_text': utils.get_datefiled_text(self.preenrolltime),
            'isoldstudent_text': '<span class="layui-badge layui-bg-blue">是</span>' if self.isoldstudent == 1 else '<span class="layui-badge">否</span>',
            'adduserlink': adduser_link,
            'isuser': '<span class="layui-badge layui-bg-blue">是</span>' if user else '<span class="layui-badge">否</span>'
        })
        return res

    @staticmethod
    def showitem():
        return {
            'showfield': [
                utils.gen_show_field('姓名', 'truename', config.SHOW_TEXT),
                utils.gen_show_field('学校', 'preenrollschool_text', config.SHOW_TEXT),
                utils.gen_show_field('年级', 'preenrollgrade_text', config.SHOW_TEXT),
                utils.gen_show_field('电话', 'phone', config.SHOW_TEXT),
                utils.gen_show_field('预报课程', 'course_text', config.SHOW_TEXT),
                utils.gen_show_field('预报名时间', 'preenrolltime_text', config.SHOW_TEXT),
                utils.gen_show_field('是否是老学员', 'isoldstudent_text', config.SHOW_HTML),
                utils.gen_show_field('是否已有用户', 'isuser', config.SHOW_HTML)
            ],
            'verbose_name': '预报名信息管理',
            'isexport': True,
            'linkfield': [
                utils.gen_link_field('adduserlink', '新建学生')
            ],
            'selectfield': [
                filedutils.gen_show_select_field('选择课程群', [], model_q='q__course__classinfo__id',
                                                 selectid='status_select',
                                                 modelname='ClassInfo', modelfunc='get_select_json'),
            ],
        }

    edititem = [
        utils.gen_edit_field('姓名', 'truename', config.EDIT_TEXT, verify=config.VERIFY_REQUIRED, helptext='请输入报名学员的姓名'),
        utils.gen_edit_field('学校', 'preenrollschool', config.EDIT_SELECT, verify=config.VERIFY_REQUIRED,
                             helptext='请选择学员的学校', modelname='SchoolInfo'),
        utils.gen_edit_field('年级', 'preenrollgrade', config.EDIT_SELECT, verify=config.VERIFY_REQUIRED,
                             helptext='请选择报名学员的年级或届次', modelname='GradeInfo'),
        utils.gen_edit_field('电话', 'phone', config.EDIT_TEXT, verify=config.VERIFY_PHONE_AND_REQUIRED,
                             helptext='请输入报名学员的电话'),
        utils.gen_edit_field('预报课程', 'course', config.EDIT_SELECT, verify=config.VERIFY_REQUIRED, helptext='请选择预报名的课程',
                             modelname='ClassCourseInfo'),
        utils.gen_edit_field('预报名时间', 'preenrolltime', config.EDIT_LAYDATE, verify=config.VERIFY_REQUIRED,
                             helptext='请选择预报名时间'),
        utils.gen_edit_field('是否是老学员', 'isoldstudent', config.EDIT_SELECT, helptext='选择是否是老学员', isforeignkey=False,
                             default=utils.gen_select_field(isoldstudent_choice_map), rel_type='no_rel'),
        utils.gen_edit_field('获取渠道', 'getpath', config.EDIT_CHECKBOX, helptext='填写获取渠道',
                             default=utils.gen_select_field(getpath_choice_map)),
        utils.gen_edit_field('备注', 'note', config.EDIT_TEXTAREA, helptext='请填写备注')
    ]

    exportlist = [
        utils.gen_export_field('姓名', 'truename'),
        utils.gen_export_field('学校', 'preenrollschool_text'),
        utils.gen_export_field('年级', 'preenrollgrade_text'),
        utils.gen_export_field('电话', 'phone'),
        utils.gen_export_field('预报课程', 'course_text'),
        utils.gen_export_field('预报名时间', 'preenrolltime_text'),
        utils.gen_export_field('是否是老学员', 'isoldstudent_export_text'),
        utils.gen_export_field('获取渠道', 'getpath_list_text'),
        utils.gen_export_field('备注', 'note')
    ]

    class Meta:
        verbose_name = '预报名信息'
        verbose_name_plural = '预报名信息'
        app_label = 'info'


class OldData(BaseModel):
    number = models.CharField(verbose_name='协议编号', max_length=255, null=True, blank=True, db_index=True)
    name = models.CharField(verbose_name='姓名', max_length=255, null=True, blank=True, db_index=True)
    sex = models.CharField(verbose_name='性别', max_length=255, null=True, blank=True)
    school = models.CharField(verbose_name='学校', max_length=255, null=True, blank=True)
    grade = models.CharField(verbose_name='年级', max_length=255, null=True, blank=True)
    studentphonenumber = models.CharField(verbose_name='学生电话', max_length=255, null=True, blank=True)
    parentphonenumber = models.CharField(verbose_name='家长电话', max_length=255, null=True, blank=True)
    homeaddress = models.CharField(verbose_name='家庭住址', max_length=255, null=True, blank=True)
    courseclass = models.CharField(verbose_name='课程班', max_length=255, null=True, blank=True)
    course1 = models.CharField(verbose_name='课程1', max_length=255, null=True, blank=True)
    course2 = models.CharField(verbose_name='课程2', max_length=255, null=True, blank=True)
    course3 = models.CharField(verbose_name='课程3', max_length=255, null=True, blank=True)
    course4 = models.CharField(verbose_name='课程4', max_length=255, null=True, blank=True)
    course5 = models.CharField(verbose_name='课程5', max_length=255, null=True, blank=True)
    course6 = models.CharField(verbose_name='课程6', max_length=255, null=True, blank=True)
    totalcost = models.CharField(verbose_name='总花费', max_length=255, null=True, blank=True)
    discount = models.CharField(verbose_name='折扣', max_length=255, null=True, blank=True)
    realcost = models.CharField(verbose_name='实际花费', max_length=255, null=True, blank=True)
    payee = models.CharField(verbose_name='收款人', max_length=255, null=True, blank=True)
    receiptnumber = models.CharField(verbose_name='收据号', max_length=255, null=True, blank=True)
    posnumber = models.CharField(verbose_name='pos单号', max_length=255, null=True, blank=True)
    entrytime = models.CharField(verbose_name='录入时间', max_length=255, null=True, blank=True)
    coursestarttime = models.CharField(verbose_name='课程开始时间', max_length=255, null=True, blank=True)
    theoryendtime = models.CharField(verbose_name='理论结束时间', max_length=255, null=True, blank=True)
    realendtime = models.CharField(verbose_name='实际结束时间', max_length=255, null=True, blank=True)
    refundstate = models.CharField(verbose_name='是否有退款', max_length=255, null=True, blank=True)
    refundmoney = models.CharField(verbose_name='退款金额', max_length=255, null=True, blank=True)
    refundtime = models.CharField(verbose_name='退款时间', max_length=255, null=True, blank=True)
    note = models.CharField(verbose_name='备注', max_length=255, null=True, blank=True)
    paytime = models.CharField(verbose_name='付款时间', max_length=255, null=True, blank=True)
    premoney = models.CharField(verbose_name='预付款', max_length=255, null=True, blank=True)
    GradePeriod = models.CharField(verbose_name='届次', max_length=255, null=True, blank=True)

    def get_json(self):
        return {
            'ordering': self.ordering,
            'id': self.id,
            'number': self.number,
            'name': self.name,
            'sex': self.sex,
            'school': self.school,
            'grade': self.grade,
            'studentphonenumber': self.studentphonenumber,
            'parentphonenumber': self.parentphonenumber,
            'homeaddress': self.homeaddress,
            'courseclass': self.courseclass,
            'course1': self.course1,
            'course2': self.course2,
            'course3': self.course3,
            'course4': self.course4,
            'course5': self.course5,
            'course6': self.course6,
            'totalcost': self.totalcost,
            'discount': self.discount,
            'realcost': self.realcost,
            'payee': self.payee,
            'receiptnumber': self.receiptnumber,
            'posnumber': self.posnumber,
            'entrytime': self.entrytime,
            'coursestarttime': self.coursestarttime,
            'theoryendtime': self.theoryendtime,
            'realendtime': self.realendtime,
            'refundstate': self.refundstate,
            'refundmoney': self.refundmoney,
            'refundtime': self.refundtime,
            'note': self.note,
            'paytime': self.paytime,
            'premoney': self.premoney,
            'GradePeriod': self.GradePeriod,
            'courselist': self.get_course_list(self.course1, self.course2, self.course3, self.course4, self.course5,
                                               self.course6),
            'phones': ('家长:' + self.parentphonenumber if self.parentphonenumber != '' else '') + (
                '<br>个人:' + self.studentphonenumber if self.studentphonenumber != '' else '')
        }

    def get_list_json(self):
        res = self.get_base_json()
        res.update({
            'GradePeriod': self.GradePeriod,
            'number': self.number,
            'name': self.name,
            'school': self.school,
            'grade': self.grade,
            'phones': ('家长:' + self.parentphonenumber if self.parentphonenumber != '' else '') + (
                '<br>个人:' + self.studentphonenumber if self.studentphonenumber != '' else '')
        })
        return res

    def get_course_list(self, *courses):
        courselist = []
        for index, course in enumerate(courses):
            if course != '' and index == 0:
                courselist.append(course)
            if course != '' and index != 0:
                courselist.append('<br>' + course)
        return ''.join(courselist)

    def __unicode__(self):
        return self.name + '-' + self.number

    @property
    def showname(self):
        return self.name + '-' + self.number

    showitem = {
        config.SHOWITEM_SHOWFIELD: [
            utils.gen_show_field('协议编号', 'number', config.SHOW_TEXT),
            utils.gen_show_field('姓名', 'name', config.SHOW_TEXT),
            utils.gen_show_field('届次', 'GradePeriod', config.SHOW_TEXT),
            utils.gen_show_field('学校', 'school', config.SHOW_TEXT),
            utils.gen_edit_field('电话', 'phones', config.SHOW_HTML)
        ],
        config.SHOWITEM_VERBOSE_NAME: '历史数据信息',
        'isexport': True
    }

    edititem = [
        utils.gen_edit_field('协议编号', 'number', config.EDIT_TEXT),
        utils.gen_edit_field('姓名', 'name', config.EDIT_TEXT),
        utils.gen_edit_field('性别', 'sex', config.EDIT_TEXT),
        utils.gen_edit_field('学校', 'school', config.EDIT_TEXT),
        utils.gen_edit_field('届次', 'GradePeriod', config.EDIT_TEXT),
        utils.gen_edit_field('年级', 'grade', config.EDIT_TEXT),
        utils.gen_edit_field('学生电话号码', 'studentphonenumber', config.EDIT_TEXT),
        utils.gen_edit_field('家长电话号码', 'parentphonenumber', config.EDIT_TEXT),
        utils.gen_edit_field('家庭住址', 'homeaddress', config.EDIT_TEXT),
        utils.gen_edit_field('课程班', 'courseclass', config.EDIT_TEXT),
        utils.gen_edit_field('课程1', 'course1', config.EDIT_TEXT),
        utils.gen_edit_field('课程2', 'course2', config.EDIT_TEXT),
        utils.gen_edit_field('课程3', 'course3', config.EDIT_TEXT),
        utils.gen_edit_field('课程4', 'course4', config.EDIT_TEXT),
        utils.gen_edit_field('课程5', 'course5', config.EDIT_TEXT),
        utils.gen_edit_field('课程6', 'course6', config.EDIT_TEXT),
        utils.gen_edit_field('总花费', 'totalcost', config.EDIT_TEXT),
        utils.gen_edit_field('折扣', 'discount', config.EDIT_TEXT),
        utils.gen_edit_field('实际花费', 'realcost', config.EDIT_TEXT),
        utils.gen_edit_field('收款人', 'payee', config.EDIT_TEXT),
        utils.gen_edit_field('收据号', 'receiptnumber', config.EDIT_TEXT),
        utils.gen_edit_field('pos单号', 'posnumber', config.EDIT_TEXT),
        utils.gen_edit_field('支付时间', 'paytime', config.EDIT_TEXT),
        utils.gen_edit_field('预付款', 'premoney', config.EDIT_TEXT),
        utils.gen_edit_field('录入时间', 'entrytime', config.EDIT_TEXT),
        utils.gen_edit_field('课程开始时间', 'coursestarttime', config.EDIT_TEXT),
        utils.gen_edit_field('理论结束时间', 'theoryendtime', config.EDIT_TEXT),
        utils.gen_edit_field('实际结束时间', 'realendtime', config.EDIT_TEXT),
        utils.gen_edit_field('是否有退款', 'refundstate', config.EDIT_TEXT),
        utils.gen_edit_field('退款金额', 'refundmoney', config.EDIT_TEXT),
        utils.gen_edit_field('退款时间', 'refundtime', config.EDIT_TEXT),
        utils.gen_edit_field('备注', 'note', config.EDIT_TEXTAREA)
    ]

    exportlist = [
        utils.gen_export_field('协议编号', 'number'),
        utils.gen_export_field('姓名', 'name'),
        utils.gen_export_field('性别', 'sex'),
        utils.gen_export_field('学校', 'school'),
        utils.gen_export_field('届次', 'GradePeriod'),
        utils.gen_export_field('年级', 'grade'),
        utils.gen_export_field('学生电话号码', 'studentphonenumber'),
        utils.gen_export_field('家长电话号码', 'parentphonenumber'),
        utils.gen_export_field('家庭住址', 'homeaddress'),
        utils.gen_export_field('课程班', 'courseclass'),
        utils.gen_export_field('课程1', 'course1'),
        utils.gen_export_field('课程2', 'course2'),
        utils.gen_export_field('课程3', 'course3'),
        utils.gen_export_field('课程4', 'course4'),
        utils.gen_export_field('课程5', 'course5'),
        utils.gen_export_field('课程6', 'course6'),
        utils.gen_export_field('总花费', 'totalcost'),
        utils.gen_export_field('折扣', 'discount'),
        utils.gen_export_field('实际花费', 'realcost'),
        utils.gen_export_field('收款人', 'payee'),
        utils.gen_export_field('收据号', 'receiptnumber'),
        utils.gen_export_field('pos单号', 'posnumber'),
        utils.gen_export_field('支付时间', 'paytime'),
        utils.gen_export_field('预付款', 'premoney'),
        utils.gen_export_field('录入时间', 'entrytime'),
        utils.gen_export_field('课程开始时间', 'coursestarttime'),
        utils.gen_export_field('理论结束时间', 'theoryendtime'),
        utils.gen_export_field('实际结束时间', 'realendtime'),
        utils.gen_export_field('是否有退款', 'refundstate'),
        utils.gen_export_field('退款金额', 'refundmoney'),
        utils.gen_export_field('退款时间', 'refundtime'),
        utils.gen_export_field('备注', 'note')
    ]

    class Meta:
        app_label = 'info'
        verbose_name_plural = '历史数据'
        verbose_name = '历史数据'


infomodels = [News, Notice, Research, Cover, SchoolInfo, GradeInfo, SchoolYearInfo, ClassInfo, ClassCourseInfo,
              CourseInfo, EnrollInfo, EnrollCourseInfo, OldData, EnrollCourseLeaveInfo, PreEnrollInfo]
