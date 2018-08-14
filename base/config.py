# coding=utf-8

searchkeyconfig = {
    'EnrollInfo': 'q__user__truename__icontains__or__no__icontains__or__parentphone__icontains',
    'User': 'q__username__icontains__or__truename__icontains__or__school__schoolname__icontains__or__grade__gradename__icontains__or__homephone__icontains__or__entryexamscore__icontains__or__entryschool__icontains',
    'SchoolInfo': 'q__schoolname__icontains',
    'GradeInfo': 'q__gradename__icontains',
    'SchoolYearInfo': 'q__schoolyearname__icontains',
    'CourseInfo': 'q__coursename__icontains',
    'ClassInfo': 'q__schoolyearinfo__schoolyearname__icontains__or__classname__icontains',
    'ClassCourseInfo': 'q__teacherinfo__truename__icontains__or__courseinfo__coursename__icontains',
    'OldData': 'q__number__icontains__or__name__icontains__or__GradePeriod__icontains__or__school__icontains__or__studentphonenumber__icontains__or__parentphonenumber__icontains',
    # 'PreEnrollInfo': 'q__preenrollschool__schoolname__icontains__or__truename__icontains',
    'PreEnrollInfo': 'q__truename__icontains__or__preenrollgrade__gradename__icontains__or__phone__icontains__or__preenrollschool__schoolname__icontains',
    'ActionLog': 'q__user__truename__icontains__or__user__username__icontains__or__content__icontains__or__model__icontains__or__model_cn__icontains__or__action__icontains'
}

"""展示字段配置"""
SHOW_TEXT = 'text'  # 普通文本
SHOW_IMG = 'img'  # 图像
SHOW_USERICON = 'usericon'  # 用户头像
SHOW_HTML = 'html'
SHOW_FILE = 'file'
SHOW_FILES = 'files'

"""编辑字段配置"""
EDIT_TEXT = 'text'
EDIT_TEXTAREA = 'textarea'
EDIT_IMG = 'img'
EDIT_USERICON = 'usericon'
EDIT_KINGEDITOR = 'kingeditor'
EDIT_WANGEDITOR = 'wangeditro'
EDIT_LAYDATE = 'laydate'
EDIT_SELECT = 'select'
EDIT_SELECT_2 = 'select_2'
EDIT_CHECKBOX = 'checkbox'
EDIT_FILE = 'file'
EDIT_FILES = 'files'

"""验证字段配置"""
VERIFY_REQUIRED = 'required'
VERIFY_PHONE = 'phone'
VERIFY_EMAIL = 'email'
VERIFY_FLOAT = 'float'
VERIFY_INT = 'int'
VERIFY_FLOAT_AND_REQUIRED = 'required|float'
VERIFY_PHONE_AND_REQUIRED = 'required|phone'
VERIFY_INT_AND_REQUIRED = 'required|int'

"""showitem字段"""
SHOWITEM_SHOWFIELD = 'showfield'
SHOWITEM_VERBOSE_NAME = 'verbose_name'
"""
老师作业：上传作业，分发给学生，打分，评语
"""

"""选择框关联字段"""
REL_TYPE_NO_REL = 'no_rel'
REL_TYPE_NO_REL_HAS_KEY = 'no_rel_has_key'


model_self_teacher = {
    'Task': 'course__teacherinfo_id',
    'TaskRecord': 'task__course__teacherinfo_id'
}

model_self_student = {

}

model_self_teacher_assistant = {
    'TeacherAssistantCourse': 'user_id'
}
