# -*- coding: UTF-8 -*-
import time
from django.db import models

# Create your models here.
from base.models import BaseModel, User
from info.models import ClassCourseInfo, EnrollCourseInfo
from base import utils, config


class Task(BaseModel):
    """作业表"""
    status_choice = [[1, '进行中'], [2, '已截止']]
    status_choice_map = dict(status_choice)

    course = models.ForeignKey(verbose_name='课程', to=ClassCourseInfo)
    taskname = models.CharField(verbose_name='作业名称', max_length=255)
    qtime = models.DateField(verbose_name='最晚提交时间')
    files = models.TextField(verbose_name='附件')
    desc = models.TextField(verbose_name='描述', null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using,
                          update_fields=update_fields)
        self.update_task_record(self.course, self)

    def update_task_record(self, course, task):
        ecis = EnrollCourseInfo.objects.filter(gradecourseinfo=course)
        for eci in ecis:
            user = eci.enrollinfo.user
            tr = TaskRecord.objects.filter(user=user, task=task)
            if not tr:
                TaskRecord(user=eci.enrollinfo.user, task=task, score=-1).save()

    @property
    def showname(self):
        return (self.course.showname if self.course else '') + '-' + self.taskname

    def __unicode__(self):
        return self.showname

    @property
    def get_doing_rate(self):
        trs = TaskRecord.objects.filter(task=self)
        ids = []
        for tr in trs:
            if tr.score and tr.score != -1:
                ids.append(tr.id)
        is_doing = trs.filter(pk__in=ids)
        return {'done_rate': '%.2f%%' % ((float(is_doing.count()) / float(trs.count())) * 100),
                'student_count': trs.count(),
                'done_count': is_doing.count()}

    def get_json(self):
        taskstatus_id = None
        if not isinstance(self.qtime, unicode):
            now = time.time()
            qtime = time.mktime(self.qtime.timetuple())
            if now < qtime:
                taskstatus_id = 1
            if now > qtime:
                taskstatus_id = 2
        self.update_task_record(self.course, self)
        res = {
            'ordering': self.ordering,
            'id': self.id,
            'name': self.showname,
            # 'course': utils.get_foreignkey_value(self.course, 'get_json'),
            'course_id': utils.get_foreignkey_value(self.course, 'id'),
            'course_text': utils.get_foreignkey_value(self.course, 'showname'),
            'taskname': self.taskname,
            'qtime_text': utils.get_datefiled_text(self.qtime),
            'qtime': self.qtime,
            'desc': self.desc,
            'taskrecord_link': "B.addWindowTab('批改" + self.showname + "','/xadmin/modellist.html?modelname=TaskRecord&q__task_id=" + str(
                self.id) + "')",
            'files': self.files,
            'taskstatus': self.status_choice_map.get(taskstatus_id) if taskstatus_id else None,
            'taskstatus_id': taskstatus_id,
        }
        res.update(self.get_doing_rate)
        return res

    def get_student_score_json(self, userid):
        res = self.get_json()
        tr = TaskRecord.objects.filter(task=self, user_id=userid).first()
        res['taskrecord'] = utils.get_foreignkey_value(tr, 'get_json')
        return res

    showitem = {
        'showfield': [
            utils.gen_show_field('课程', 'course_text', config.SHOW_TEXT),
            utils.gen_show_field('作业名', 'taskname', config.SHOW_TEXT),
            utils.gen_show_field('状态', 'taskstatus', config.SHOW_HTML),
            utils.gen_show_field('总人数', 'student_count', config.SHOW_TEXT),
            utils.gen_show_field('完成人数', 'done_count', config.SHOW_TEXT),
            utils.gen_show_field('完成率', 'done_rate', config.SHOW_TEXT),
            utils.gen_show_field('最晚提交时间', 'qtime_text', config.SHOW_TEXT)
        ],
        'verbose_name': '课程作业',
        'linkfield': [
            utils.gen_link_field(None, '<span style="color:gray;">&nbsp;|&nbsp;</span>', islink=False),
            utils.gen_link_field('taskrecord_link', '批改'),
        ],
        'headopfield': [
            utils.gen_headop_field('导出所有作业情况', 'export_course_task()', 'btn btn-primary radius size-S')
        ]
    }

    edititem = [
        utils.gen_edit_field('课程', 'course', config.EDIT_SELECT, verify=config.VERIFY_REQUIRED, helptext='选择课程',
                             modelname='ClassCourseInfo', disabled=True, defaultselect_q='q__course_id'),
        utils.gen_edit_field('作业名', 'taskname', config.EDIT_TEXT, verify=config.VERIFY_REQUIRED, helptext='输入作业名'),
        utils.gen_edit_field('最晚提交时间', 'qtime', config.EDIT_LAYDATE, verify=config.VERIFY_REQUIRED, helptext='选择期限时间'),
        utils.gen_edit_field('附件', 'files', config.EDIT_FILE, helptext='添加附件，注意：只能添加一个附件，如果是多个文件，请压缩后上传'),
        utils.gen_edit_field('描述', 'desc', config.EDIT_TEXTAREA, helptext='输入描述')
    ]

    class Meta:
        app_label = 'student'
        verbose_name_plural = '课程作业'
        verbose_name = '课程作业'


class TaskRecord(BaseModel):
    """作业记录"""
    score_choice = [[0, '未批改'], [1, '已批改']]
    score_choice_map = dict(score_choice)

    user = models.ForeignKey(verbose_name='用户', to=User)
    task = models.ForeignKey(verbose_name='作业', to=Task)
    score = models.IntegerField(verbose_name='成绩')
    feedback = models.TextField(verbose_name='反馈', null=True, blank=True)

    @property
    def showname(self):
        return self.task.showname + '-' + self.user.showname + '分值'

    def __unicode__(self):
        return self.showname

    def get_json(self):
        score_id = None
        if self.score != -1:
            score_id = 1
        else:
            score_id = 0
        return {
            'ordering': self.ordering,
            'id': self.id,
            'name': self.showname,
            # 'user': utils.get_foreignkey_value(self.user, 'get_json'),
            'user_id': utils.get_foreignkey_value(self.user, 'id'),
            'user_text': utils.get_foreignkey_value(self.user, 'showname'),
            # 'task': utils.get_foreignkey_value(self.task, 'get_json'),
            'task_id': utils.get_foreignkey_value(self.task, 'id'),
            'task_text': utils.get_foreignkey_value(self.task, 'taskname'),
            'score_id': score_id,
            'score_text': self.score_choice_map.get(score_id),
            'score': self.score if score_id == 1 else '',
            'feedback': self.feedback
        }

    edititem = [
        utils.gen_edit_field('用户', 'user', config.EDIT_SELECT, verify=config.VERIFY_REQUIRED, helptext='选择用户',
                             modelname='User', disabled=True),
        utils.gen_edit_field('作业', 'task', config.EDIT_SELECT, verify=config.VERIFY_REQUIRED, helptext='选择作业',
                             modelname='Task', disabled=True, defaultselect_q='q__task_id'),
        utils.gen_edit_field('分值', 'score', config.EDIT_TEXT, verify=config.VERIFY_INT_AND_REQUIRED,
                             helptext='输入分值，输入一个整数'),
        utils.gen_edit_field('评语', 'feedback', config.EDIT_TEXTAREA, helptext='请输入评语')
    ]

    showitem = {
        'showfield': [
            utils.gen_show_field('用户', 'user_text', config.SHOW_TEXT),
            # utils.gen_show_field('作业', 'task_text', config.SHOW_TEXT),
            utils.gen_show_field('分值', 'score', config.SHOW_TEXT)
        ],
        'verbose_name': '作业记录'
    }

    class Meta:
        app_label = 'student'
        verbose_name = '作业记录'
        verbose_name_plural = '作业记录'


# class TaskSubject(BaseModel):
#     """作业题目"""
#     task = models.ForeignKey(verbose_name='作业', to=Task)
#     subjectname = models.TextField(verbose_name='题目名称', max_length=255)
#     subjectfile = models.TextField(verbose_name='题目文件')
#
#     @property
#     def showname(self):
#         return self.task.showname + '-' + self.subjectname
#
#     def __unicode__(self):
#         return self.showname
#
#     def get_json(self):
#         return {
#             'id': self.id,
#             'task': utils.get_foreignkey_value(self.task, 'get_json'),
#             'task_id': utils.get_foreignkey_value(self.task, 'id'),
#             'task_text': utils.get_foreignkey_value(self.task, 'showname'),
#             'subjectname': self.subjectname,
#             'subjectfile': self.subjectfile
#         }
#
#     edititem = [
#         utils.gen_edit_field('作业', 'task', config.EDIT_SELECT, verify=config.VERIFY_REQUIRED, helptext='选择作业',
#                              modelname='Task',disabled=True,defaultselect_q='q__task_id'),
#         utils.gen_edit_field('题目名称', 'subjectname', config.EDIT_TEXT, verify=config.VERIFY_REQUIRED,
#                              helptext='请输入题目名称'),
#         utils.gen_edit_field('题目文件', 'subjectfile', config.EDIT_FILE, verify=config.VERIFY_REQUIRED, helptext='请上传文件')
#     ]
#
#     showitem = {
#         'showfield': [
#             utils.gen_show_field('作业', 'task_text', config.SHOW_TEXT),
#             utils.gen_show_field('题目名称', 'subjectname', config.SHOW_TEXT),
#             utils.gen_show_field('文件', 'subjectfile', config.SHOW_FILE)
#         ],
#         'verbose_name': '作业题目'
#     }
#
#     class Meta:
#         ordering = ['-id']
#         app_label = 'student'
#         verbose_name = '作业题目'
#         verbose_name_plural = '作业题目'
#
#
studentmodels = [Task, TaskRecord]
