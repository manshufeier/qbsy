/**
 * Created by stone on 2017/7/21.
 */

Vue.component('vue-page', {
    delimiters: ['[[', ']]'],
    props: ['total', 'startitem', 'enditem', 'onchange'],
    template: '<div style="margin-top: 2px;display: none;" id="page_area">\
            共&nbsp;<span style="color: green;">[[total]]</span>&nbsp;条&nbsp;|&nbsp;当前显示：<span style="color: green;">[[startitem]]</span>~<span\
                style="color: green;">[[enditem]]</span>&nbsp;|&nbsp;\
            每页显示：\
            <span class="select-box radius size-S" style="width: 100px;">\
                <select class="select" id="select_page"\
                        :onchange="onchange">\
                    <option value="5">5条</option>\
                    <option value="10" selected>10条(默认)</option>\
                    <option value="15">15条</option>\
                    <option value="20">20条</option>\
                    <option value="50">50条</option>\
                </select>\
            </span>\
            <span id="page"></span></div>',
});

Vue.component('vue-search', {
    delimiters: ['[[', ']]'],
    props: ['id', 'onload'],
    template: '<span style="float: right;">\
                        <input type="text" :id="id" style="width:150px" class="input-text radius size-S" :oninput="onload">\
                        <button name="" id="" class="btn btn-success radius size-S"\
                             :onclick="onload"><i\
                             class="Hui-iconfont">&#xe665;</i> 搜索</button>\
                     </span>',
});

Vue.component('vue-upload-btn', {
    delimiters: ['[[', ']]'],
    props: ['onchange', 'text', 'id'],
    template: '<span class="btn-upload" style="height: 27px;">\
                        <a href="javascript:void(0);" class="btn btn-primary radius size-S"><i class="Hui-iconfont">&#xe642;</i>&nbsp;[[text]]</a>\
                            <input type="file" class="input-file" :id="id"\
                                :onchange="onchange">\
                      </span>'
});

Vue.component('vue-upload-extro', {
    delimiters: ['[[', ']]'],
    props: ['onchange', 'text', 'id'],
    template: '<span class="btn-upload" style="height: 25px;">\
                            <i class="iconfont  icon-fileadd" style="font-size: 25px;color: rgba(0,0,0,0.58);"></i>添加附件\
                            <input type="file" class="input-file" :id="id"\
                                :onchange="onchange">\
                      </span>'
});

Vue.component('vue-select', {
    delimiters: ['[[', ']]'],
    props: ['id', 'name', 'items','placeholder'],
    template: '<select class="select" :id="id" :name="name">\
                        <option value="" disabled selected style="display:none;">[[placeholder]]</option>  \
                        <option :value="item.id" v-for="item in items">[[item.name]]</option>\
                    </select>'
});


Vue.component('vue-table', {
    delimiters: ['[[', ']]'],
    props: ['items','showfield'],
    template: '<table class="table table-border table-bg table-bordered table-hover" style="margin-top: 10px;">\
            <thead>\
            <tr>\
                <th width="5%"><input id="select_checkbox" type="checkbox"\
                                      onclick="B.gen_select_all(\'select_checkbox\',\'select_elem\');"></th>\
                <th v-for="field in showfield">[[field]]</th>\
                <th>操作</th>\
            </tr>\
            </thead>\
            <tbody>\
            <tr v-for="item in items" onclick="B.select_selected(this);">\
                <th class="sel"><input type="checkbox" :id="item.sel_id" name="select_elem" onclick="B.select_selected($(this).parent().parent());"></th>\
                <td v-for="(value,key) in item" v-if="key!=\'sel_id\' && key!=\'edit_link\' ">[[value]]</td>\
                <td><a href="javascript:void(0);" :onclick="item.edit_link">编辑</a></td>\
            </tr>\
        </table>'
});