#coding=utf8

def get_app_models():
    from base.models import Role, User, KeyValue, ActionLog
    from student.models import studentmodels
    from exam.models import exam_models
    from teacher.models import teacher_models
    from info.models import infomodels
    return [Role, User, KeyValue, ActionLog] + studentmodels + exam_models + teacher_models + infomodels


def getModel(modelname):
    if type(modelname) == type:
        model = modelname
    else:
        modelname = modelname.lower()
        modelsmap = {}
        for m in get_app_models():
            modelsmap[m._meta.model_name.lower()] = m
        model = modelsmap.get(modelname)
    return model
