# coding=utf8
from django.db import models

# Create your models here.
from base.models import BaseModel, User
from info.models import ClassCourseInfo
from base import utils, config


class TeacherAssistantCourse(BaseModel):
    """教辅课程"""
    user = models.ForeignKey(verbose_name='用户', to=User)
    course = models.ForeignKey(verbose_name='课程', to=ClassCourseInfo)
    des = models.TextField(verbose_name='描述', null=True, blank=True)

    @property
    def showname(self):
        return '{0}-{1}'.format(self.user.showname, self.course.showname)

    def __unicode__(self):
        return self.showname

    def get_json(self):
        res = self.get_base_json()
        res.update({
            'name': self.showname,
            'user': None,
            'course': None,
            'user_id': utils.get_foreignkey_value(self.user, 'id'),
            'user_text': utils.get_foreignkey_value(self.user, 'showname'),
            'course_id': utils.get_foreignkey_value(self.course, 'id'),
            'course_text': utils.get_foreignkey_value(self.course, 'showname'),
            'des': self.des,
            'q__classinfo__id': self.course.classinfo.id if self.course and self.course.classinfo else None,
            'taskmgr_link': "B.addWindowTab('" + self.course.showname + "作业管理','/xadmin/modellist.html?modelname=Task&q__course_id=" + str(
                self.course.id) + "')",
        })
        return res

    showitem = {
        'showfield': [
            utils.gen_show_field('用户', 'user_text', config.SHOW_TEXT),
            utils.gen_show_field('课程', 'course_text', config.SHOW_TEXT),
            utils.gen_show_field('描述', 'des', config.SHOW_TEXT)
        ],
        'verbose_name': '教辅课程',
        'linkfield': [
            utils.gen_link_field(None, '<span style="color:gray;">&nbsp;|&nbsp;</span>', islink=False),
            utils.gen_link_field('taskmgr_link', '作业管理')
        ]
    }

    edititem = [
        utils.gen_edit_field('用户', 'user', config.EDIT_SELECT, verify=config.VERIFY_REQUIRED, helptext='选择用户',
                             isforeignkey=True, modelname='User', querydic={'role_id': 6}, disabled=True,
                             defaultselect_q='q__user_id'),
        utils.gen_edit_field('课程', 'course', config.EDIT_SELECT_2, verify='required',
                             helptext='选择课程班课程信息', select_two_query_filter='q__classinfo__id',
                             modelname='ClassCourseInfo', select_one_text='请选择课程群', select_two_text='请选择课程',
                             select_one_modelname='ClassInfo', select_two_modelname='ClassCourseInfo'),
        utils.gen_edit_field('描述', 'des', config.EDIT_TEXTAREA, helptext='可以输入大致的描述')
    ]

    class Meta:
        app_label = 'teacher'
        verbose_name = '教辅课程'
        verbose_name_plural = verbose_name


teacher_models = [TeacherAssistantCourse]
