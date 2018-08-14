#coding=utf8
from django.db import models

# Create your models here.

from base.models import BaseModel,User,config
from base import utils
from info.models import CourseInfo

class Exam(BaseModel):
    """考试信息"""
    user=models.ForeignKey(verbose_name='用户',to=User)
    examname=models.CharField(verbose_name='考试名称',max_length=255)
    examsubject=models.ForeignKey(verbose_name='考试科目',to=CourseInfo,null=True,blank=True,on_delete=models.SET_NULL)
    score=models.CharField(verbose_name='分数',max_length=20)
    subjectclassranking=models.CharField(verbose_name='科目班级排名',max_length=20,null=True,blank=True)
    classranking=models.CharField(verbose_name='综合班级排名',max_length=20,null=True,blank=True)
    subjectgraderanking=models.CharField(verbose_name='科目年级排名',max_length=20,null=True,blank=True)
    graderanking=models.CharField(verbose_name='综合年级排名',max_length=20,null=True,blank=True)
    analysis=models.TextField(verbose_name='分析',null=True,blank=True)

    @property
    def showname(self):
        return self.examname

    def __unicode__(self):
        return self.showname

    def get_json(self):
        return {
            'ordering': self.ordering,
            'id':self.id,
            'name':self.examname,
            'user_id':self.user.id,
            'user_text':self.user.showname,
            'examsubject_id':utils.get_foreignkey_value(self.examsubject,'id'),
            'examsubject_text':utils.get_foreignkey_value(self.examsubject,'showname'),
            'examname':self.examname,
            'score':self.score,
            'subjectclassranking':self.subjectclassranking,
            'classranking':self.classranking,
            'subjectgraderanking':self.subjectgraderanking,
            'graderanking':self.graderanking,
            'analysis':self.analysis
        }

    edititem=[
        utils.gen_edit_field('用户','user',config.EDIT_SELECT,disabled=True,verify=config.VERIFY_REQUIRED,helptext='选择用户',modelname='User',defaultselect_q='q__user_id'),
        utils.gen_edit_field('考试名称','examname',config.EDIT_TEXT,verify=config.VERIFY_REQUIRED,helptext='请输入这次考试的名称'),
        utils.gen_edit_field('考试科目','examsubject',config.EDIT_SELECT,verify=config.VERIFY_REQUIRED,helptext='请选择考试的科目',modelname='CourseInfo'),
        utils.gen_edit_field('成绩','score',config.EDIT_TEXT,verify=config.VERIFY_REQUIRED,helptext='输入学生的成绩，输入一个整数或小数'),
        utils.gen_edit_field('科目班级排名','subjectclassranking',config.EDIT_TEXT,helptext='请输入科目班级排名'),
        utils.gen_edit_field('班级排名','classranking',config.EDIT_TEXT,helptext='请输入班级排名'),
        utils.gen_edit_field('科目年级排名','subjectgraderanking',config.EDIT_TEXT,helptext='请输入年级科目排名'),
        utils.gen_edit_field('年级排名','graderanking',config.EDIT_TEXT,helptext='请输入年级排名'),
        utils.gen_edit_field('试卷分析','analysis',config.EDIT_TEXTAREA,helptext='请输入对试卷的分析')
    ]

    showitem={
        'showfield':[
            utils.gen_show_field('用户','user_text',config.SHOW_TEXT),
            utils.gen_show_field('考试名称','examname',config.SHOW_TEXT),
            utils.gen_show_field('考试科目','examsubject_text',config.SHOW_TEXT),
            utils.gen_show_field('成绩','score',config.SHOW_TEXT),
            utils.gen_show_field('科目班级排名','subjectclassranking',config.SHOW_TEXT),
            utils.gen_show_field('班级排名','classranking',config.SHOW_TEXT),
            utils.gen_show_field('科目年级排名','subjectgraderanking',config.SHOW_TEXT),
            utils.gen_show_field('年级排名','graderanking',config.SHOW_TEXT)
        ],
        'verbose_name':'成绩统计'
    }

    class Meta:
        app_label='exam'
        verbose_name_plural='成绩记录'
        verbose_name='成绩记录'

exam_models=[Exam]