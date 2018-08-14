# -*- coding: UTF-8 -*-
import json

import types

from base import modelinfo


def get_queryfilters(param, trans=None):
    q = {}
    for k in param:
        if k.startswith("q__"):
            v = param[k]
            if v:
                q[k[3:]] = v if not trans or v not in trans else trans[v]
    return q


def get_pageinfo(param, size=10, page=1):
    size = 'size' in param and int(param['size']) or size
    if size < 0:
        size = 100000
    page = 'page' in param and int(param['page']) or page
    start = size * (page - 1)
    return (size, page, start)


def warp_query(query, trans=None, param=None):
    if param:
        qs = get_queryfilters(param, trans)
        from django.db.models import Q
        nqs = {}
        Q()
        for k, v in qs.items():
            if '__or__' in k:
                ks = k.split('__or__')
                for k in ks:
                    if not query[0].get_json().has_key((k.split('__')[0])):
                        ks.remove(k)
                print ks
                q = Q(**{ks[0]: v})
                for nk in ks[1:]:
                    q = q | Q(**{nk: v})
                query = query.filter(q)
            else:
                nqs[k] = v
        if nqs:
            query = query.filter(**nqs)

    if param and 'sort' in param:
        query = query.order_by(u'%s%s' % ('-' if 'order' in param and param['order'] == 'desc' else '', param['sort']))
    if param and 'orderby' in param:
        query = query.order_by(*[v.strip() for v in param['orderby'].split(',') if v.strip()])
    return query


def gen_pager(query, trans=None, size=10, page=1, param=None):
    start = 0
    if param:
        size, page, start = get_pageinfo(param, size, page)
    else:
        size, page = int(size), int(page)
        start = size * (page - 1)
    query = warp_query(query, trans, param)
    count = query.count()
    rawquery = query
    items = query[start:size * page]
    firstpage = 1
    lastpage = (count - 1) / size + 1
    res = {
        'itemsquery': items,
        'rawquery': rawquery,
        'items': items,
        'count': count,
        'page': page,
        'size': size,
        'start': start,
        'prevpage': page - 1 if page > 1 else 1,
        'nextpage': page + 1 if page < lastpage else lastpage,
        'prev': page - 1 if page > 1 else False,
        'next': page + 1 if page < lastpage else False,
        'first': firstpage if page > firstpage else False,
        'last': lastpage if page < lastpage else False,
        'lastpage': lastpage,
        'firstpage': firstpage,
    }
    res['needpager'] = res['next'] or res['prev']
    return res


def gen_pager_array(query, trans=None, size=10, page=1, param=None, func=None, extra_dic=None):
    res = gen_pager(query, trans, size, page, param)
    items = res['items']
    start = res['start']
    count = res['count']
    return Array(items=[o if not func else func(o) for o in items], start=start, total=count, rawquery=res['rawquery'],
                 extra_dic=extra_dic)


def gen_query_json_list_array(query, param, showitem=None, funcstr=None, funcdic=None, extra_dic=None, listfields=None):
    query = warp_query(query, param=param)
    data = gen_json_list_array(query, param=param, showitem=showitem, funcstr=funcstr, funcdic=funcdic,
                               extra_dic=extra_dic, listfields=listfields)
    return data


def gen_query_json(query, param=None, extra_dic=None):
    query = warp_query(query, param=param)
    data = query.first().get_json()
    if (extra_dic):
        data.update(extra_dic)
    return data


def gen_json_list_array(query, size=10, page=1, param=None, showitem=None, funcstr=None, funcdic=None,
                        extra_dic=None, listfields=None):
    if param:
        size = int(param['size']) if 'size' in param else size
        if size < 0:
            size = 100000
        page = 'page' in param and int(param['page']) or page
        start = size * (page - 1)
    else:
        if size < 0:
            size = 100000
        size, page = int(size), int(page)
        start = size * (page - 1)
    queryitems = query[start:size * page] if size != 0 else []
    items = [(i if isinstance(i, dict) else i.get_json() if not funcstr else getattr(i, funcstr)(**funcdic)) for i in
             queryitems]
    data = Array(items, total=query.count() if not isinstance(query, list) else len(query), start=start,
                 showitem=showitem, extra_dic=extra_dic)
    return data


def obj2dic(o, ks, d=None):
    if d == None:
        d = {}
    for k in ks:
        d[k] = getattr(o, k)
    return d


def dic2obj(o, ks, d):
    """
    字典转化为对象，需提供fields
    @param o: 
    @param ks: 
    @param d: 
    @return: 
    """
    for k in ks:
        if k in d:
            #             print '%s:%s'%(k,d[k])
            setattr(o, k, d[k])


def dic2obj_nofield(o, dic):
    """
    字典转化为对象模型，无需提供fields
    @param o: 
    @param dic: 
    @return: 
    """
    for k, v in dic.items():
        setattr(o, k, v)


def obj2obj(dst, ks, src):
    for k in ks:
        if hasattr(src, k):
            setattr(dst, k, getattr(src, k))


class ApiException(BaseException):
    pass


def ex(e, c=-1):
    return ApiException({"code": c, "msg": e})


class Data(object):
    def __init__(self, data=None):
        self.data = data


class Array(Data):
    @property
    def data(self):
        res = {"items": self.items, "start": self.start, "total": self.total, 'showitem': self.showitem}
        if self.extra_dic:
            res.update(self.extra_dic)
        return res

    def __init__(self, items, start=0, total=-1, rawquery=None, showitem=None, extra_dic=None):
        self.items = items
        self.start = start
        self.total = total if total != -1 else len(items)
        self.rawquery = rawquery
        self.showitem = showitem
        self.extra_dic = extra_dic


def json_filed_default(obj):
    import decimal
    import datetime
    import time
    from django.db.models.fields.files import ImageFieldFile
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    if isinstance(obj, datetime.datetime):
        return obj.timetuple()
    if isinstance(obj, datetime.date):
        return obj.timetuple()
    if isinstance(obj, time.struct_time):
        return {"timestamp": time.mktime(obj), "date": time.strftime('%Y-%m-%d', obj)}
    if isinstance(obj, ImageFieldFile):
        if hasattr(obj, 'url'):
            return obj.url
        else:
            return ''
    raise TypeError(type(obj))


def get_one_by_sql(sql, params=None, db=None):
    from django.db import connection, transaction
    cursor = connection[db].cursor() if db else connection.cursor()
    cursor.execute(sql, params)
    r = cursor.fetchone()
    cursor.close()
    return r


def objstrip(obj):
    if type(obj) == dict:
        keys = obj.keys()
        for k in keys:
            if not obj[k]:
                del obj[k]
            else:
                objstrip(obj[k])
    elif type(obj) == list or type(obj) == tuple:
        for o in obj:
            objstrip(o)
    return obj


def splitstrip(strs, seg=' '):
    if not strs:
        return []
    return [s.strip() for s in strs.split(seg) if s.strip()]


def orderinggen():
    import time
    return max(int(time.time()), 0)


class Ix(object):
    _index = -1

    @property
    def start(self):
        self._index = 0
        return self._index

    @property
    def next(self):
        self._index += 1
        return self._index

    def span(self, v):
        v -= 1
        self._index += v
        return self._index

    @property
    def index(self):
        return self._index


def gen_rndstr(s, l=6):
    import random
    return ''.join([random.choice(s) for _ in range(l)])


def verify_phone_format(phone):
    """
    验证电话号码格式
    @param phone: 
    @return: 
    """
    import re
    p2 = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
    if p2.match(phone):
        return True
    else:
        raise ex(u'手机号码格式不正确:%s' % phone)


def get_request_dic(request_data):
    """
    获取请求的字典
    @param request_data: 
    @return: 
    """
    dic = {}
    for key in request_data:
        dic.update({key: str(request_data[key])})
    return dic


def gen_edit_field(showname, name, type, disabled=None, verify=None, helptext=None, default=None, rel_type='is_rel',
                   modelname=None, querydic=None, defaultselect_q=None, defaultselect=None, isforeignkey=True,
                   select_one_text=None, select_two_text=None, select_one_modelname=None, select_two_modelname=None,
                   select_two_query_filter=None, showkey=None, showvalue=None, is_edit_show=True):
    """
    构建编辑字段
    @param showname: 
    @param name: 
    @param type: 
    @param disabled: 
    @param verify: 
    @param helptext: 
    @param default: 
    @param rel_type: 
    @return: 
    """
    return set_none_dic(showname=showname,
                        name=name,
                        type=type,
                        disabled=disabled,
                        verify=verify,
                        helptext=helptext,
                        default=default,
                        rel_type=rel_type,
                        modelname=modelname,
                        querydic=querydic,
                        defaultselect_q=defaultselect_q,
                        defaultselect=defaultselect,
                        isforeignkey=isforeignkey,
                        select_one_text=select_one_text,
                        select_two_text=select_two_text,
                        select_one_modelname=select_one_modelname,
                        select_two_modelname=select_two_modelname,
                        select_two_query_filter=select_two_query_filter,
                        showkey=showkey,
                        showvalue=showvalue,
                        is_edit_show=is_edit_show)


def set_none_dic(**dic):
    res = {}
    for key, value in dic.items():
        if value:
            res[key] = value
    return res


def gen_export_field(showname, fieldname):
    return {
        'showname': showname,
        'fieldname': fieldname
    }


def gen_data_field(name, type):
    """
    构建data字段
    @param name: 
    @param type: 
    @return: 
    """
    return {'name': name, 'type': type}


def gen_link_field(name, linkname, showkey=None, showvalue=None, islink=True):
    """
    构建链接字段
    @param name: 
    @param linkname: 
    @return: 
    """
    return {'name': name, 'linkname': linkname, 'showkey': showkey, 'showvalue': showvalue, 'islink': islink}


def gen_show_field(showname, name, type, showkey=None, showvalue=None):
    """
    构建展示字段
    @param showname: 
    @param name: 
    @param type: 
    @return: 
    """
    return {'showname': showname, 'name': name, 'type': type, 'showkey': showkey, 'showvalue': showvalue}


def gen_headop_field(text, op, _class):
    """
    构建顶部操作栏字段
    @param text: 
    @param op: 
    @param _class: 
    @return: 
    """
    return {'text': text, 'op': op, 'class': _class}


def gen_select_field(list_map):
    """
    获取选择的字段
    @param list_map: 
    @return: 
    """
    select_field = []
    for key, value in list_map.items():
        select_field.append({'id': key, 'name': value})
    return select_field


def get_img_info(filepath, imgtype, is_compress=True):
    """
    获取img_info
    @param filepath: 
    @param imgtype: 
    @param is_compress: 
    @return: 
    """
    from PIL import Image
    import os
    filepath = filepath if filepath[0] != '/' else filepath[1:]
    file_array = str(filepath).split('.')
    filetype = file_array[-1]
    times = 0
    img_path = ''
    if imgtype == 'small' or imgtype == 'middle':
        img_path = filepath + '.' + imgtype + '.' + filetype
    if imgtype == 'normal':
        img_path = filepath
    if imgtype == 'small':
        times = 4
    if imgtype == 'middle':
        times = 2
    if not os.path.exists(filepath):
        return None
    sImg = Image.open(filepath)
    w, h = sImg.size
    if imgtype == 'small' or imgtype == 'middle':
        if is_compress:
            img = sImg.resize((w / times, h / times), Image.ANTIALIAS)
            img.save(img_path)
            w, h = img.size
        else:
            sImg = Image.open(img_path)
            w, h = sImg.size
    url = '/' + img_path
    img_info = {'url': url, 'size': os.path.getsize(img_path), 'width': w, 'height': h}
    return img_info


def get_full_compress_img_info(filepath):
    """
    获取压缩后的完整img_info
    @param filepath: 
    @return: 
    """
    return {'normal_info': get_img_info(filepath, 'normal'), 'small_info': get_img_info(filepath, 'small')}


def get_full_img_info(filepath):
    """
    得到完整的img_info
    @param filepath: 
    @return: 
    """
    res = None
    if filepath != None:
        if filepath != '' and filepath != 'null':
            res = {'normal_info': get_img_info(filepath, 'normal', is_compress=False),
                   'small_info': get_img_info(filepath, 'small', is_compress=False)}
    return res


def get_full_imgs_info(filepaths):
    """
    得到多图片的image_info
    @param filepaths: 
    @return: 
    """
    path_arr = str(filepaths).split(',')
    json_arr = []
    for path in path_arr[0:-1]:
        json_arr.append(get_full_img_info(path))
    return json_arr


def get_uid(id):
    """
    通过id获取uid
    @param id: 
    @return uid: 
    """
    return 100000000 + id + 10000


def get_id(uid):
    """
    通过uid获取id
    @param uid: 
    @return id: 
    """
    return uid - 100000000 - 10000


def get_datefiled_text(datafiled):
    """
    从django模型的datefiled中获取对应的时间string
    :param datafiled: 
    :return: 
    """
    if datafiled == None:
        return ''
    if isinstance(datafiled, unicode):
        return datafiled
    else:
        return datafiled.strftime('%Y-%m-%d')


def get_foreignkey_value(modelfield, subfield, subfielddic=None):
    if modelfield:
        if hasattr(modelfield, subfield):
            if isinstance(getattr(modelfield, subfield), types.MethodType):
                return getattr(modelfield, subfield)() if not subfielddic else getattr(modelfield, subfield)(
                    **subfielddic)
            else:
                return getattr(modelfield, subfield)
        else:
            return None
    else:
        return None


def is_json_list(jsonstr):
    try:
        if not jsonstr or jsonstr == '' or not isinstance(json.loads(jsonstr), list):
            return False
        json.loads(jsonstr)
    except ValueError:
        return False
    return True
