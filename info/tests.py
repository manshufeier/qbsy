# coding=utf8
from django.test import TestCase
import json

# Create your tests here.

read_to_json = lambda path: json.loads((open(path)).read())


def main():
    from info.models import OldData
    from qbsy import settings
    json_src = read_to_json(settings.BASE_DIR + '/static/datatemp/data.json')
    for index,js in enumerate(json_src):
        print u'正在存取第%d条数据'%(index+1)
        OldData(**js).save()
    print u'处理完成'
