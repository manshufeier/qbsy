+function (B, $) {

    B.callapi = function (m, p, succ, fail, async) {
        if (!p)
            p = {};
        $.ajax({
            url: '/api/' + m,
            type: B.DEBUG ? 'GET' : 'POST',
            dataType: 'JSON',
            data: p,
            async: async,
            success: function (res) {
                if (res.code == 0) {
                    if (succ)
                        succ(res);
                }
                else {
                    if (res.code == 1000) {

                    }
                    else {
                        if (fail) {
                            if (!fail(res)) {
                                B.close_loading();
                                layer.alert(res.msg, {title: '提示'})
                            }
                        }
                        else {
                            if (!succ || !succ(null)) {
                                B.close_loading();
                                layer.alert(res.msg, {title: '错误'});
                            }
                        }
                    }
                }
            },
            error: function (e) {
                if (fail)
                    fail(e);
                else if (succ) {
                    console.log(e);
                    B.close_loading();
                    layer.alert('操作失败，请检查网络!', {title: '错误'})
                    succ(null);
                }
            }
        });
    };

    B.getDatetime = function (tstamp) {
        //功能：把unix时间戳转成Y-m-d H:i:s格式的日期
        var now = new Date(tstamp * 1000);
        var year = now.getFullYear();
        var month = now.getMonth() + 1;
        month = month < 10 ? "0" + month : month;
        var day = now.getDate();
        day = day < 10 ? "0" + day : day;
        var hour = now.getHours();
        hour = hour < 10 ? "0" + hour : hour;
        var minute = now.getMinutes();
        minute = minute < 10 ? "0" + minute : minute;
        var second = now.getSeconds();
        second = second < 10 ? "0" + second : second;
        return year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second;
    };

    B.getLocalDateTime = function (tstamp) {
        return B.getDatetime(tstamp).replace(' ', 'T');
    };

    B.getLocalDate = function (tstamp) {
        var datetime = B.getDatetime(tstamp);
        return datetime.substring(0, datetime.indexOf(' '));
    };

    B.display_loading = function () {
        loading_temp = '<div style="z-index:1000;padding-top:10px;color:darkblue;position:fixed;right:0;left:0;margin:auto;width:25px; height:25px;" class="loading-icon">' +
            '<i class="layui-icon layui-anim layui-anim-rotate layui-anim-loop" style="display:inline-block;font-size: 25px;">&#xe63d;</i></div>';
        if ($('.loading-icon', window.parent.document).length == 0) {
            if ($('.loading-icon').length == 0) {
                $(document.body).before(loading_temp);
                $('.loading-icon').show();
            }
        }
    };

    B.close_loading = function () {
        $('.loading-icon').hide().remove();
        $('.loading-icon', window.parent.document).hide().remove();
    };

    B.addWindowTab = function (title, url, icon) {
        if (window.top.addTab)
            window.top.addTab(title, url, icon);
        else {
            window.open(url);
        }
    };

    B.gen_page = function (pageid, pageindex, pagesize, total, func) {

        layui.use(['laypage', 'layer'], function () {
            var laypage = layui.laypage;
            laypage.render({
                elem: pageid
                , count: total
                , limit: pagesize
                , curr: pageindex || 1
                , layout: ['count', 'prev', 'page', 'next', 'limit', 'skip']
                , jump: function (obj, first) {
                    if (!first) {
                        func(obj.curr, obj.limit);
                        scrollTo(0, 0);
                    }
                }
            });
        });

    };

    B.gen_select_all = function (checkbox_id, select_elem_name) {
        var select_elem_list = $("input[name=" + select_elem_name + "]");
        if ($('#' + checkbox_id).is(':checked')) {
            for (var i = 0; i < select_elem_list.size(); i++) {
                $(select_elem_list[i]).prop('checked', true);
                $(select_elem_list[i]).parent().parent().addClass('success');
            }
        } else {
            for (var i = 0; i < select_elem_list.size(); i++) {
                $(select_elem_list[i]).prop('checked', false);
                $(select_elem_list[i]).parent().parent().removeClass('success');
            }
        }
    };

    B.get_select_ids = function (select_elem_name) {
        var select_ids = [];
        $("input[name=" + select_elem_name + "]").each(function (v) {
            if ($(this).is(':checked')) {
                select_ids.push($(this).attr('id').substring(4));
            }
        });
        if (select_ids.length == 0) {
            layer.open({title: '提示', content: '没有选中任何数据'});
        }
        return select_ids;
    };

    B.del_datas = function (select_elem_name, modelname, func) {
        ids = B.get_select_ids(select_elem_name);
        if (ids.length > 0) {
            layer.confirm('确定要删除' + ids.length + '条数据么？', {icon: 3, title: '提示'}, function (index) {
                Base.callapi("delModels", {modelname: modelname, ids: ids.join(',')}, function (res) {
                    if (res && res.data) {
                        layer.msg('操作成功！！！', {icon: 1});
                        func();
                        var select_elem_list = $("input[name=" + select_elem_name + "]");
                        for (var i = 0; i < select_elem_list.size(); i++) {
                            $(select_elem_list[i]).prop('checked', false);
                            $(select_elem_list[i]).parent().parent().removeClass('success');
                        }
                    }
                });
            });
        }
    };

    B.top_datas = function (select_elem_name, modelname, func) {
        ids = B.get_select_ids(select_elem_name);
        if (ids.length > 0) {
            Base.callapi("topModels", {modelname: modelname, ids: ids.join(',')}, function (res) {
                if (res && res.data) {
                    func();
                    var select_elem_list = $("input[name=" + select_elem_name + "]");
                    for (var i = 0; i < select_elem_list.size(); i++) {
                        $(select_elem_list[i]).prop('checked', false);
                        $(select_elem_list[i]).parent().parent().removeClass('success');
                    }
                }
            });
        }
    };


    function on_progress(evt) {
        if (evt.lengthComputable) {
            var percent = Math.round((evt.loaded) * 100 / evt.total);
            layui.use('element', function () {
                var element = layui.element;
                element.progress('progress', percent + '%');
            });
        }
    }


    function upload_files_com(url, fileid, func) {
        var progress_templ = '\
            <div style="background-color:#f5fafe;border:1px solid #5a98de;position:fixed;margin:auto;left:0; right:0; top:0; bottom:0;width:300px; height:30px;padding:5px;" class="uploading">\
            <div style="width:300px;" class="layui-progress" lay-filter="progress">\
                <div class="layui-progress-bar layui-bg-blue" lay-percent="0%"></div></div>\
                <span style="width:100px;margin:auto;" id="upload_text">上传中...</span></div>';
        $(document.body).append(progress_templ);
        var xhr = new XMLHttpRequest();
        // var file = document.getElementById(fileid).files[0];
        var files = document.getElementById(fileid).files;
        var form = new FormData();
        // form.append('file', file);
        for (var i = 0; i < files.length; i++) {
            form.append(files[i].name, files[i]);
        }
        xhr.upload.addEventListener('progress', on_progress, false);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    res = JSON.parse(xhr.responseText);
                    if (res.code == 0) {
                        setTimeout(function () {
                            $('.uploading').remove();
                            $('#' + fileid).val('');
                            func(res);
                        }, 1000);
                    } else {
                        setTimeout(function () {
                            $('.uploading').remove();
                            $('#' + fileid).val('');
                            layer.open({title: '提示', content: res.msg});
                        }, 1000);
                    }
                } else {
                    setTimeout(function () {
                        $('.uploading').remove();
                        $('#' + fileid).val('');
                        layer.open({title: '提示', content: '上传失败，请检查网络'});
                    }, 1000);
                }
            }
        };
        xhr.open('POST', url, true);
        xhr.setRequestHeader('X-CSRFTOKEN', '{{ request.COOKIES.csrftoken }}');
        xhr.send(form);
    }

    function upload_com(url, fileid, func) {
        var progress_templ = '\
            <div style="background-color:#f5fafe;border:1px solid #5a98de;position:fixed;margin:auto;left:0; right:0; top:0; bottom:0;width:300px; height:30px;padding:5px;" class="uploading">\
            <div style="width:300px;" class="layui-progress" lay-filter="progress">\
                <div class="layui-progress-bar layui-bg-blue" lay-percent="0%"></div></div>\
                <span style="width:100px;margin:auto;" id="upload_text">上传中...</span></div>';
        $(document.body).append(progress_templ);
        var xhr = new XMLHttpRequest();
        var file = document.getElementById(fileid).files[0];
        var form = new FormData();
        form.append('file', file);
        xhr.upload.addEventListener('progress', on_progress, false);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    res = JSON.parse(xhr.responseText);
                    if (res.code == 0) {
                        setTimeout(function () {
                            $('.uploading').remove();
                            $('#' + fileid).val('');
                            func(res);
                        }, 1000);
                    } else {
                        setTimeout(function () {
                            $('.uploading').remove();
                            $('#' + fileid).val('');
                            layer.open({title: '提示', content: res.msg});
                        }, 1000);
                    }
                } else {
                    setTimeout(function () {
                        $('.uploading').remove();
                        $('#' + fileid).val('');
                        layer.open({title: '提示', content: '上传失败，请检查网络'});
                    }, 1000);
                }
            }
        };
        xhr.open('POST', url, true);
        xhr.setRequestHeader('X-CSRFTOKEN', '{{ request.COOKIES.csrftoken }}');
        xhr.send(form);
    }

    B.upload = function (fileid, func) {
        upload_com('/api/upload_file', fileid, func);
    };

    B.upload_files = function (fileid, func) {
        upload_files_com('/api/upload_files', fileid, func);
    };


    B.upload_subject = function (fileid, func) {
        upload_com('/api/upload_subjects', fileid, func);
    };

    B.upload_user = function (fileid, func) {
        upload_com('/api/upload_users', fileid, func);
    };

    B.gen_data = function (func) {
        var isadd = true;
        if (B.getQueryString('isadd') == -1) {
            isadd = false;
        }
        var isdeleted = true;
        if (B.getQueryString('isdelete') == -1) {
            isdeleted = false;
        }
        var isedit = true;
        if (B.getQueryString('isedit') == -1) {
            isedit = false;
        }
        params = {
            items: [],
            total: null,
            pagesize: 20,
            pageindex: 1,
            startitem: null,
            enditem: null,
            showfield: [],
            linkfield: [],
            verbose_name: '',
            headopfield: [],
            is_deleted: isdeleted,
            is_edit: isedit,
            show_op: true,
            is_add: isadd,
            selectfield: [],
            isexport: false
        };
        func(params);
        return params;
    };

    B.gen_loadData = function (app, api, params, pageid, pageindex, pagesize, func, async) {
        B.display_loading();
        var thiz = app.$data;
        thiz.pagesize = pagesize;
        thiz.pageindex = pageindex;
        params.size = thiz.pagesize;
        params.page = thiz.pageindex;
        B.callapi(api, params, function (res) {
            if (res && res.data && res.data.items) {
                thiz.total = res.data.total;
                if (parseInt(pageindex - 1) * pagesize >= parseInt(thiz.total)) {
                    thiz.pageindex = Math.ceil(thiz.total / pagesize);
                    app.loadData(thiz.pageindex, thiz.pagesize);
                    return;
                }
                if (res.data.showitem && res.data.showitem.showfield) {
                    thiz.showfield = res.data.showitem.showfield;
                    for (var i = 0; i < thiz.showfield.length; i++) {
                        thiz.showfield[i].showkeyvalue = B.getQueryString(thiz.showfield[i].showkey);
                    }
                }
                if (res.data.showitem && res.data.showitem.linkfield) {
                    thiz.linkfield = res.data.showitem.linkfield;
                }
                if (res.data.showitem && res.data.showitem.verbose_name) {
                    thiz.verbose_name = res.data.showitem.verbose_name;
                }
                if (res.data.showitem && res.data.showitem.is_deleted != null) {
                    thiz.is_deleted = res.data.showitem.is_deleted;
                }
                if (res.data.showitem && res.data.showitem.show_op != null) {
                    thiz.show_op = res.data.showitem.show_op;
                }
                if (res.data.showitem && res.data.showitem.is_add != null) {
                    thiz.is_add = res.data.showitem.is_add;
                }
                if (res.data.showitem && res.data.showitem.is_edit != null) {
                    thiz.is_edit = res.data.showitem.is_edit;
                }
                if (res.data.showitem && res.data.showitem.headopfield) {
                    thiz.headopfield = res.data.showitem.headopfield;
                }
                if (res.data.showitem && res.data.showitem.selectfield) {
                    thiz.selectfield = res.data.showitem.selectfield;
                }
                if (res.data.showitem && res.data.showitem.isexport) {
                    thiz.isexport = res.data.showitem.isexport;
                }
                thiz.items = res.data.items;
                thiz.startitem = res.data.start + 1;
                thiz.enditem = (parseInt(thiz.pagesize) + parseInt(thiz.startitem) - 1) >= parseInt(thiz.total) ? parseInt(thiz.total) : parseInt(thiz.pagesize) + parseInt(thiz.startitem) - 1;
                if (pageid != null) {
                    B.gen_page(pageid, pageindex, pagesize, thiz.total, app.loadData);
                }
                for (var i = 0; i < thiz.items.length; i++) {
                    thiz.items[i].sel_id = 'sel_' + thiz.items[i].id;
                }
                func(thiz);
                if ((thiz.pagesize >= thiz.total) && (pageindex == 0 || pageindex == 1)) {
                    $('#page_area').hide();
                } else {
                    $('#page_area').show();
                }
                B.close_loading();
            }
        }, null, async);
    };

    B.gen_vue = function (appid, pageid, dataparams, api, apiparams, func, async) {
        var app = new Vue({
            delimiters: ['[[', ']]'],
            el: appid,
            data: dataparams,
            methods: {
                loadData: function (pageindex, pagesize) {
                    B.gen_loadData(app, api, apiparams, pageid, pageindex, pagesize, function (thiz) {
                        func(thiz);
                    }, async);
                }
            }
        });
        return app;
    };

    function gen_layui_select(selectSelect, dataValue) {
        const option_list = selectSelect.parent().find('.layui-form-select').find('.layui-anim-upbit').find('dd');
        for (var k = 0; k < option_list.length; k++) {
            if ($(option_list[k]).attr('lay-value') == dataValue) {
                $(option_list[k]).addClass('layui-this');
                selectSelect.parent().find('.layui-unselect').val($(option_list[k]).text());
            } else {
                $(option_list[k]).removeClass('layui-this');
            }
        }
        selectSelect.val(dataValue);
    }

    B.gen_edit = function (api, params, queryid, elemname) {
        B.display_loading();
        if (B.getQueryString(queryid)) {
            B.callapi(api, params, function (res) {
                if (res) {
                    const input_list = $("[name='" + elemname + "']");
                    for (var i = 0; i < input_list.size(); i++) {
                        const inputId = $(input_list[i]).attr('id');
                        const inputProperty = $(input_list[i]).attr('property');
                        const inputTagName = $(input_list[i])[0].tagName;
                        const inputType = $(input_list[i]).attr('type');
                        const inputIdSelect = $('#' + $(input_list[i]).attr('id'));
                        if (inputTagName === 'SELECT') {
                            if (inputProperty === 'no_rel') {
                                gen_layui_select(inputIdSelect, res.data[inputId]);
                            } else if (inputProperty === 'select_2') {
                                var select_one = inputIdSelect.parent().parent().find('[select_two_query_filter]');
                                gen_layui_select(select_one, res.data[select_one.attr('select_two_query_filter')]);
                                gen_layui_select(inputIdSelect, res.data[inputId + '_id']);
                            }
                            else {
                                gen_layui_select(inputIdSelect, res.data[inputId + '_id']);
                            }
                        }
                        else if (inputTagName == 'TEXTAREA') {
                            if (inputProperty == 'kingeditor') {
                                KindEditor.ready(function (K) {
                                    var editor = K.create('#' + inputId, {
                                        cssPath: 'plugins/code/prettify.css',
                                        uploadJson: '/kingeditor/kingeditor_upload',
                                        allowFileManager: true
                                    });
                                    prettyPrint();
                                    editor.html(res.data[inputId]);
                                });
                            } else {
                                inputIdSelect.val(res.data[inputId]);
                            }

                        } else if (inputTagName == 'DIV') {
                            if (inputProperty == 'ueditor') {
                                var content = UE.getEditor(inputId, {
                                    'initialFrameWidth': null,
                                    'initialFrameHeight': 200,
                                    'serverUrl': '/ueditor/controller/?imagePathFormat=ueditor%2Fimg%2F&filePathFormat=ueditor%2Ffile%2F'
                                });
                                var ue_content = res.data[inputId];
                                content.ready(function () {
                                    content.setContent(ue_content, false);
                                });
                            } else if (inputProperty == 'extro_file') {
                                var file_list_id = $(input_list[i]).find('#extro_file_list');
                                var file_list_data = JSON.parse(res.data[inputId]);
                                for (var j = 0; j < file_list_data.length; j++) {
                                    $(file_list_id).append('<div><a href="' + file_list_data[j].url + '" class="btn-link" name="extro_file" download="' +
                                        file_list_data[j].filename + '">' + file_list_data[j].filename + '</a><i class="Hui-iconfont Hui-iconfont-close" style="float:right;" onclick="$(this).parent().remove();"></i></div>');
                                }
                            }
                            else if (inputProperty == 'wangeditor') {
                                var E = window.wangEditor;
                                var editor = new E('#' + inputId);
                                editor.customConfig.uploadImgServer = '/wangeditor/uploadimg';
                                editor.create();
                                editor.txt.html(res.data[inputId]);
                            } else if (inputProperty == 'rolecheckbox') {
                                const checkboxs = inputIdSelect.find('input');
                                const layuicheckboxs = inputIdSelect.find('.layui-form-checkbox');
                                const opration_list = JSON.parse(res.data[inputId]);
                                for (var k = 0; k < checkboxs.length; k++) {
                                    if ($.inArray($(checkboxs[k]).attr('k'), opration_list) !== -1) {
                                        $(checkboxs[k]).attr('checked', 'checked');
                                        $(layuicheckboxs[k]).addClass('layui-form-checked');
                                    }
                                }
                            }
                            else if (inputProperty == 'modelconfig') {
                                var permission_json = JSON.parse(res.data[inputId]);
                                const modelElems = inputIdSelect.find('[modelname]');
                                for (var k = 0; k < modelElems.length; k++) {
                                    var modelname = $(modelElems[k]).attr('modelname');
                                    var modelitem = permission_json[modelname];
                                    var checkboxs = $(modelElems[k]).next().find('input');
                                    const layuicheckboxs = $(modelElems[k]).next().find('.layui-form-checkbox');
                                    for (var m = 0; m < checkboxs.length; m++) {
                                        if (modelitem[$(checkboxs[m]).attr('k_name')]) {
                                            $(checkboxs[m]).attr('checked', 'checked');
                                            $(layuicheckboxs[m]).addClass('layui-form-checked');
                                        }
                                    }
                                }
                            }
                            else if (inputProperty == 'checkbox') {
                                const checkboxs = inputIdSelect.find('input');
                                const layuicheckboxs = inputIdSelect.find('.layui-form-checkbox');
                                const datalist = JSON.parse(res.data[inputId]);
                                for (var k = 0; k < checkboxs.length; k++) {
                                    if ($.inArray($(checkboxs[k]).attr('k'), datalist) !== -1) {
                                        $(checkboxs[k]).attr('checked', 'checked');
                                        $(layuicheckboxs[k]).addClass('layui-form-checked');
                                    }
                                }
                            }
                            else if (inputProperty == 'img') {
                                var img_url = res.data[$(input_list[i]).find('input').attr('id')];
                                var img_array = img_url.split('.');
                                var img_type = img_array[img_array.length - 1];
                                $(input_list[i]).find('img').attr('src', img_url + '.small.' + img_type);
                                $(input_list[i]).find('img').attr('img-src', img_url);
                            } else if (inputProperty == 'imgs') {
                                var img_info_list = res.data[$(input_list[i]).find('input').attr('id')];
                                for (var k = 0; k < img_info_list.length; k++) {
                                    B.insert_single_img_templ($(input_list[i]).find('input').attr('id'), img_info_list[k].normal_info.url, img_info_list[k].small_info.url);
                                }
                            }
                        }
                        else {
                            if (inputType == 'text') {
                                if (inputProperty == 'text') {
                                    inputIdSelect.val(res.data[inputId]);
                                } else if (inputProperty == 'laydate') {
                                    if (res.data[inputId] && res.data[inputId].date) {
                                        inputIdSelect.val(res.data[inputId].date);
                                    }
                                    laydate.render({
                                        elem: '#' + inputId
                                    });
                                }
                            }
                            if (inputType == 'datetime-local') {
                                inputIdSelect.val(B.getLocalDateTime(res.data[inputId].timestamp));
                            }
                            if (inputType == 'date') {
                                inputIdSelect.val(B.getLocalDate(res.data[inputId].timestamp));
                            }
                            if (inputType == 'file') {
                                var p_name = inputIdSelect.attr('p_name');
                                if (p_name == 'file') {
                                    var fileinfo = JSON.parse(res.data[inputId]);
                                    $(inputIdSelect.parent().find('a')).attr('href', fileinfo.url);
                                    $(inputIdSelect.parent().find('a')).attr('download', fileinfo.filename);
                                    $(inputIdSelect.parent().find('a')).html(fileinfo.filename);
                                } else if (p_name == 'files') {
                                    var file_list_json = JSON.parse(res.data[inputId]);
                                    for (var k = 0; k < file_list_json.length; k++) {
                                        $('#' + inputId).parent().find('[k_name=file_list]').append('<div>\
                                            <a download="' + file_list_json[k].filename + '" aname="a_file" style="color:darkcyan;" href="' + file_list_json[k].url + '">' + file_list_json[k].filename + '</a>\
                                            <i class="Hui-iconfont Hui-iconfont-close" style="float:right;"\
                                                onclick="$(this).parent().remove();"></i>\
                                            </div>');
                                    }
                                }
                            }
                        }
                    }
                    B.close_loading();
                }
            });
        }
        else {
            var input_list = $("[name='" + elemname + "']");
            for (var i = 0; i < input_list.size(); i++) {
                var inputId = $(input_list[i]).attr('id');
                var inputProperty = $(input_list[i]).attr('property');
                var inputTagName = $(input_list[i])[0].tagName;
                var inputType = $(input_list[i]).attr('type');
                const inputIdSelect = $('#' + $(input_list[i]).attr('id'));
                if (inputTagName == 'SELECT') {
                    if ($(input_list[i]).is('[select_name]')) {
                        var select_name = $(input_list[i]).attr('select_name');
                        inputIdSelect.val(B.getQueryString(select_name));
                    }
                    if ($(input_list[i]).is('[defaultselect]')) {
                        var defaultselct = $(input_list[i]).attr('defaultselect');
                        inputIdSelect.val(defaultselct);
                    }
                } else if (inputTagName == 'TEXTAREA') {
                    if (inputProperty == 'kingeditor') {
                        KindEditor.ready(function (K) {
                            var editor = K.create('#' + inputId, {
                                cssPath: 'plugins/code/prettify.css',
                                uploadJson: '/kingeditor/kingeditor_upload',
                                allowFileManager: true
                            });
                            prettyPrint();
                        });
                    }
                } else if (inputTagName == 'DIV') {
                    if (inputProperty == 'ueditor') {
                        var content = UE.getEditor(inputId, {
                            'initialFrameWidth': null,
                            'initialFrameHeight': 200,
                            'serverUrl': '/ueditor/controller/?imagePathFormat=ueditor%2Fimg%2F&filePathFormat=ueditor%2Ffile%2F'
                        });
                    }
                    else if (inputProperty == 'extro_file') {
                    }
                    else if (inputProperty == 'wangeditor') {
                        var E = window.wangEditor;
                        var editor = new E('#' + inputId);
                        editor.customConfig.uploadImgServer = '/wangeditor/uploadimg';
                        editor.create();
                    }
                }
                else {
                    if (inputType == 'text' || inputType == 'password') {
                        if (inputProperty == 'text' || inputProperty == 'password') {
                            if ($(input_list[i]).is('[defaultselect_q]')) {
                                var defaultselect_q = $(input_list[i]).attr('defaultselect_q');
                                inputIdSelect.val(B.getQueryString(defaultselect_q));
                            }
                        } else if (inputProperty == 'laydate') {
                            laydate.render({
                                elem: '#' + inputId
                            });
                        }
                    }
                    if (inputType == 'datetime-local') {
                    }
                    if (inputType == 'date') {
                        var date = new Date();
                        var dateString = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
                        inputIdSelect.val(dateString);
                    }
                }
            }
        }
        B.close_loading();
    };

    B.save_data = function (api, params, queryid, elemname, func) {
        B.display_loading();
        var data = params;
        if (params == null) {
            data = {};
        }
        var input_list = $("[name='" + elemname + "']");
        for (var i = 0; i < input_list.size(); i++) {
            var inputId = $(input_list[i]).attr('id');
            var inputProperty = $(input_list[i]).attr('property');
            var inputTagName = $(input_list[i])[0].tagName;
            var inputType = $(input_list[i]).attr('type');
            const inputIdSelect = $('#' + $(input_list[i]).attr('id'));
            if (inputTagName === 'SELECT') {
                if (inputProperty == 'no_rel' || inputProperty == 'no_rel_has_key') {
                    data[inputId] = inputIdSelect.val();
                }
                else {
                    data[inputId + '_id'] = inputIdSelect.val();
                }
            }
            else if (inputTagName == 'TEXTAREA') {
                if (inputProperty == 'kingeditor') {
                    data[inputId] = inputIdSelect.parent().find('.ke-edit-iframe').contents().find('body').html()
                } else {
                    data[inputId] = inputIdSelect.val();
                }

            }
            else if (inputTagName == 'DIV') {
                if (inputProperty == 'ueditor') {
                    var content = UE.getEditor(inputId, {
                        'initialFrameWidth': null,
                        'initialFrameHeight': 200,
                        'serverUrl': '/ueditor/controller/?imagePathFormat=ueditor%2Fimg%2F&filePathFormat=ueditor%2Ffile%2F'
                    });
                    content.ready(function () {
                        data[inputId] = content.getContent();
                    });
                } else if (inputProperty == 'extro_file') {
                    var file_list = $(input_list[i]).find('#extro_file_list').children();
                    var files = [];
                    for (var j = 0; j < file_list.length; j++) {
                        var file = {};
                        file.filename = $(file_list[j]).find('a').text();
                        file.url = $(file_list[j]).find('a').attr('href');
                        files.push(file);
                    }
                    data[inputId] = JSON.stringify(files);
                }
                else if (inputProperty == 'wangeditor') {
                    data[inputId] = inputIdSelect.find('.w-e-text').html();
                }
                else if (inputProperty == 'rolecheckbox') {
                    const checkboxs = inputIdSelect.find('input');
                    // const layuicheckboxs = inputIdSelect.find('.layui-form-checkbox');
                    var data_opration_list = [];
                    for (var k = 0; k < checkboxs.length; k++) {
                        if ($(checkboxs[k]).is(':checked')) {
                            data_opration_list.push($(checkboxs[k]).attr('k'));
                        }
                    }
                    data[inputId] = JSON.stringify(data_opration_list);
                } else if (inputProperty == 'modelconfig') {
                    const modelElems = inputIdSelect.find('[modelname]');
                    model_json = {};
                    for (var k = 0; k < modelElems.length; k++) {
                        var modelname = $(modelElems[k]).attr('modelname');
                        m_item = {};
                        var checkboxs = $(modelElems[k]).next().find('input');
                        for (var m = 0; m < checkboxs.length; m++) {
                            m_item[$(checkboxs[m]).attr('k_name')] = $(checkboxs[m]).is(':checked');
                        }
                        model_json[$(modelElems[k]).attr('modelname')] = m_item;
                    }
                    data[inputId] = JSON.stringify(model_json);
                }
                else if (inputProperty == 'checkbox') {
                    const checkboxs = inputIdSelect.find('input');
                    var datalist = [];
                    for (var k = 0; k < checkboxs.length; k++) {
                        if ($(checkboxs[k]).is(':checked')) {
                            datalist.push($(checkboxs[k]).attr('k'));
                        }
                    }
                    data[inputId] = JSON.stringify(datalist);
                }
                else if (inputProperty == 'img') {
                    data[$(input_list[i]).find('input').attr('id')] = $(input_list[i]).find('img').attr('img-src');
                } else if (inputProperty == 'imgs') {
                    var img_list = $(input_list[i]).find('[s_name=single_img]');
                    var imgs_str = "";
                    for (var k = 0; k < img_list.length; k++) {
                        imgs_str += $(img_list[k]).attr('img_src') + ',';
                    }
                    data[$(input_list[i]).find('input').attr('id')] = imgs_str;
                }
            }
            else {
                if (inputType == 'text' || inputType == 'password' || inputType == 'laydate') {
                    data[inputId] = inputIdSelect.val();
                }
                if (inputType == 'datetime-local') {
                    data[inputId] = inputIdSelect.val();
                }
                if (inputType == 'date') {
                    data[inputId] = inputIdSelect.val();
                }
                if (inputType == 'file') {
                    var p_name = inputIdSelect.attr('p_name');
                    if (p_name == 'file') {
                        if (inputIdSelect.parent().find('a').attr('href') != null) {
                            data[inputId] = JSON.stringify({
                                filename: inputIdSelect.parent().find('a').html(),
                                url: inputIdSelect.parent().find('a').attr('href')
                            });
                        }
                    } else if (p_name == 'files') {
                        var file_list = inputIdSelect.parent().find('[k_name=file_list]').children();
                        var file_json = [];
                        for (var k = 0; k < file_list.length; k++) {
                            var s_file = $(file_list[k]).find('a');
                            file_json.push({filename: $(s_file).html(), url: $(s_file).attr('href')});
                        }
                        data[inputId] = JSON.stringify(file_json);
                    }
                }
            }
        }
        if (B.getQueryString(queryid)) {
            data.id = B.getQueryString(queryid);
        }
        func(data);
        B.callapi(api, data, function (res) {
            if (res) {
                B.close_loading();
                layer.msg('保存成功！！！', {icon: 1});
                if (B.getQueryString('isremoved') == -1) {
                    removeIframe();
                }
            }
        });
    }

    B.select_selected = function (tr) {
        if (!$(tr).find('input').is(':checked')) {
            $(tr).find('input').prop('checked', true);
            $(tr).addClass('success');
        } else {
            $(tr).find('input').prop('checked', false);
            $(tr).removeClass('success');
            $(tr).parent().parent().find('thead').find('tr').find('input').prop('checked', false);
        }
    };

    B.we_img_upload = function (fileid, func) {
        upload_files_com('/wangeditor/uploadimg', fileid, func);
    };

    B.urlEncode = function (params) {
        var paramStr = '';
        for (p in params) {
            paramStr += '&' + p + '=' + params[p];
        }
        return paramStr;
    };

    B.urlEncodeAll = function (params) {
        return B.urlEncode(params).replace('&', '?');
    };

    B.showHuiDialog = function (title, msg, callback) {
        layer.confirm(msg, {
            title: title,
            btn: ['确认', '取消'] //按钮
        }, function () {
            if (typeof(callback) == 'function') {
                callback();
            }
        }, function () {

        });
    }

    B.unlock_user = function (modelname, func) {
        ids = B.get_select_ids('select_elem');
        if (ids.length > 0) {
            layer.confirm('确定要激活' + ids.length + '个用户么？', {icon: 3, title: '提示'}, function (index) {
                Base.callapi("backUsers", {ids: ids.join(','), modelname: modelname}, function (res) {
                    if (res) {
                        layer.msg('操作成功！！！', {icon: 1});
                        func();
                    }
                });
            });
        }
    };

    B.lock_user = function (modelname, func) {
        ids = B.get_select_ids('select_elem');
        if (ids.length > 0) {
            layer.confirm('确定要锁定' + ids.length + '个用户么？', {icon: 3, title: '提示'}, function (index) {
                Base.callapi("cancelUsers", {ids: ids.join(','), modelname: modelname}, function (res) {
                    if (res) {
                        layer.msg('操作成功！！！', {icon: 1});
                        func();
                    }
                });
            });
        }
    };

    B.insert_single_img_templ = function (elem, img_url, small_img_url) {
        templ = '<span style="display: inline-block;position: relative;width: 30%;padding-bottom: 10px;margin-right:5px;">\
                        <img src="' + small_img_url + '" img_src="' + img_url + '"\
                             style="width: 100%;height: auto;" s_name="single_img">\
                        <a href="#"\
                           style="z-index: 100;position: absolute;top: -5px;right: -5px;line-height: 16px;text-decoration: none;">\
                            <i class="layui-icon"\
                               onclick="$(this).parent().parent().remove();"\
                               style="">&#x1007;</i>\
                        </a>\
                    </span>';
        $('#' + elem).before(templ);
    };

    B.export_excel = function (params) {
        B.display_loading();
        B.callapi('export_to_excel', params, function (res) {
            if (res && res.data) {
                B.close_loading();
                window.location.href = res.data;
            }
        })
    };

    B.addfiles = function (elemid) {
        B.upload_files(elemid, function (res) {
            for (var i = 0; i < res.data.length; i++) {
                $('#' + elemid).parent().find('[k_name=file_list]').append('<div>\
                        <a download="' + res.data[i].filename + '" aname="a_file" style="color:darkcyan;" href="' + res.data[i].url + '">' + res.data[i].filename + '</a>\
                        <i class="Hui-iconfont Hui-iconfont-close" style="float:right;"\
                           onclick="$(this).parent().remove();"></i>\
                    </div>');
            }
        });
    };

}(IR, jQuery);

B = Base = IR;