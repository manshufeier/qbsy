# coding=utf8
from base import modelinfo


def gen_show_select_field(selectname, selectlist, model_q, selectid, modelname=None, modelfunc=None, modelfundic=None):
    res = {
        'selectname': selectname,
        'model_q': model_q,
        'selectid': selectid
    }
    model = modelinfo.getModel(modelname)
    if model:
        selectlist = []
        query = model.objects.filter()
        if modelfunc:
            selectlist = [getattr(q, modelfunc)() for q in query] if not modelfundic else [
                getattr(q, modelfundic)(**modelfundic) for q in query]
        else:
            selectlist = [q.get_json() for q in query]
        res['selectlist'] = selectlist
    else:
        res['selectlist'] = selectlist
    return res
