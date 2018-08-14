import json

from django.http import HttpResponse


def wangeditor_imgupload(request):
    import time, os, datetime
    file_url_list=[]
    data = {}
    if request.method == "POST":
        upload_root = 'media/WEditor'
        now = datetime.datetime.now()
        uplaod_path = os.path.join(upload_root, str(now.year) + str(now.month))
        if not os.path.exists(uplaod_path):
            os.mkdir(uplaod_path)
        for filename in request.FILES:
            file=request.FILES.get(filename,None)
            filename_h = str(int(round(time.time() * 1000))) + '.' + file.name.split('.')[-1]
            f= open(os.path.join(uplaod_path, filename_h), 'wb')
            for chunk in file.chunks():
                f.write(chunk)
            f.close()
            file_url_list.append('/' + uplaod_path + '/' +filename_h)
        data = {'data':file_url_list, 'errno': 0}
    return HttpResponse(json.dumps(data), content_type='application/json')

def kingeditor_upload(request):
    import time, os, datetime
    data = {}
    if request.method == "POST":
        upload_root = 'media/WEditor'
        now = datetime.datetime.now()
        uplaod_path = os.path.join(upload_root, str(now.year) + str(now.month))
        if not os.path.exists(uplaod_path):
            os.mkdir(uplaod_path)
        file = request.FILES.get('imgFile', None)
        filename_h = str(int(round(time.time() * 1000))) + '.' + file.name.split('.')[-1]
        f = open(os.path.join(uplaod_path, filename_h), 'wb')
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        url='/' + uplaod_path + '/' +filename_h
        data = {'url':url, 'error': 0}
    return HttpResponse(json.dumps(data), content_type='application/json')
