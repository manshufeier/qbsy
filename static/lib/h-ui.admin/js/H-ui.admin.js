/* -----------H-ui前端框架-------------
 * H-ui.admin.js v3.0
 * http://www.h-ui.net/
 * Created & Modified by guojunhui
 * Date modified 2017.02.03
 * Copyright 2013-2017 北京颖杰联创科技有限公司 All rights reserved.
 * Licensed under MIT license.
 * http://opensource.org/licenses/MIT
 */
var num = 0, oUl = $("#min_title_list"), hide_nav = $("#Hui-tabNav");

var showIndex = 0;

/*获取顶部选项卡总长度*/
function tabNavallwidth() {
    var taballwidth = 0,
        $tabNav = hide_nav.find(".acrossTab"),
        $tabNavWp = hide_nav.find(".Hui-tabNav-wp"),
        $tabNavitem = hide_nav.find(".acrossTab li"),
        $tabNavmore = hide_nav.find(".Hui-tabNav-more");
    if (!$tabNav[0]) {
        return
    }
    $tabNavitem.each(function (index, element) {
        taballwidth += Number(parseFloat($(this).width() + 60))
    });
    $tabNav.width(taballwidth + 25);
    var w = $tabNavWp.width();
    if (taballwidth + 25 > w) {
        $tabNavmore.show()
    }
    else {
        $tabNavmore.hide();
        $tabNav.css({left: 0})
    }
}

/*左侧菜单响应式*/
function Huiasidedisplay() {
    if ($(window).width() >= 768) {
        $(".Hui-aside").show()
    }
}

/*获取皮肤cookie*/
function getskincookie() {
    var v = $.cookie("Huiskin");
    var hrefStr = $("#skin").attr("href");
    if (v == null || v == "") {
        v = "default";
    }
    if (hrefStr != undefined) {
        var hrefRes = hrefStr.substring(0, hrefStr.lastIndexOf('skin/')) + 'skin/' + v + '/skin.css';
        $("#skin").attr("href", hrefRes);
    }
}

/*菜单导航*/
function Hui_admin_tab(obj) {
    var bStop = false,
        bStopIndex = 0,
        href = $(obj).attr('data-href'),
        title = $(obj).attr("data-title"),
        topWindow = $(window.parent.document),
        show_navLi = topWindow.find("#min_title_list li"),
        iframe_box = topWindow.find("#iframe_box");
    //console.log(topWindow);
    if (!href || href == "") {
        // alert("data-href不存在，v2.5版本之前用_href属性，升级后请改为data-href属性");
        return false;
    }
    if (!title) {
        // alert("v2.5版本之后使用data-title属性");
        return false;
    }
    if (title == "") {
        // alert("data-title属性不能为空");
        return false;
    }
    show_navLi.each(function () {
        if ($(this).find('span').attr("data-href") == href) {
            bStop = true;
            bStopIndex = show_navLi.index($(this));
            return false;
        }
    });
    if (!bStop) {
        creatIframe(href, title);
        min_titleList();
    }
    else {
        show_navLi.removeClass("active").eq(bStopIndex).addClass("active");
        iframe_box.find(".show_iframe").hide().eq(bStopIndex).show();
        var ifms = iframe_box.find('.show_iframe').find('iframe');
        if (ifms.length > 0) {
            var cw = ifms[bStopIndex].contentWindow;
            if (cw.onTabSelected)
                cw.onTabSelected();
        }
        // iframe_box.find(".show_iframe").hide().eq(bStopIndex).show().find("iframe").attr("src", href);
    }
}

/*最新tab标题栏列表*/
function min_titleList() {
    var topWindow = $(window.parent.document),
        show_nav = topWindow.find("#min_title_list"),
        aLi = show_nav.find("li");
}

/*创建iframe*/
function creatIframe(href, titleName) {
    var topWindow = $(window.parent.document),
        show_nav = topWindow.find('#min_title_list'),
        iframe_box = topWindow.find('#iframe_box'),
        iframeBox = iframe_box.find('.show_iframe'),
        $tabNav = topWindow.find(".acrossTab"),
        $tabNavWp = topWindow.find(".Hui-tabNav-wp"),
        $tabNavmore = topWindow.find(".Hui-tabNav-more");
    var taballwidth = 0;
    var show_item = show_nav.find('.active');
    showIndex = $(show_item).index();
    show_nav.find('li').removeClass("active");
    show_item.after('<li class="active"><span data-href="' + href + '">' + titleName + '</span><i></i><em></em></li>');
    // show_nav.append('<li class="active"><span data-href="' + href + '">' + titleName + '</span><i></i><em></em></li>');

    if ('function' == typeof $('#min_title_list li').contextMenu) {
        $("#min_title_list li").contextMenu('Huiadminmenu', {
            bindings: {
                'closethis': function (t) {
                    var $t = $(t);
                    if ($t.find("i")) {
                        $t.find("i").trigger("click");
                    }
                },
                'closeall': function (t) {
                    $("#min_title_list li i").trigger("click");
                },
            }
        });
    } else {

    }
    var $tabNavitem = topWindow.find(".acrossTab li");
    if (!$tabNav[0]) {
        return
    }
    $tabNavitem.each(function (index, element) {
        taballwidth += Number(parseFloat($(this).width() + 60))
    });
    $tabNav.width(taballwidth + 25);
    var w = $tabNavWp.width();
    if (taballwidth + 25 > w) {
        oUl.animate({'left': -(oUl.width() - $tabNavWp.width())}, 100);
        $tabNavmore.show()
    }
    else {
        $tabNavmore.hide();
        $tabNav.css({left: 0})
    }
    var showBox1 = iframe_box.find('.show_iframe:visible');
    iframeBox.hide();
    if ($('.dislpayArrow').find('.open').length === 0) {
        showBox1.after('<div class="show_iframe"><div style="padding-top:10px;color:darkblue;position:fixed;right:0;left:199px;margin:auto;width:25px; height:25px;" class="loading-icon">' +
            '<i class="layui-icon layui-anim layui-anim-rotate layui-anim-loop" style="display:inline-block;font-size: 25px;">&#xe63d;</i></div><iframe frameborder="0" src=' + href + '></iframe></div>');
    } else {
        showBox1.after('<div class="show_iframe"><div style="padding-top:10px;color:darkblue;position:fixed;right:0;left:0;margin:auto;width:25px; height:25px;" class="loading-icon">' +
            '<i class="layui-icon layui-anim layui-anim-rotate layui-anim-loop" style="display:inline-block;font-size: 25px;">&#xe63d;</i></div><iframe frameborder="0" src=' + href + '></iframe></div>');
    }
    var showBox = iframe_box.find('.show_iframe:visible');
    showBox.find('iframe').load(function () {
        showBox.find('.loading').hide();
    });
}

/*关闭iframe*/
function removeIframe() {
    var topWindow = $(window.parent.document),
        iframe = topWindow.find('#iframe_box .show_iframe'),
        tab = topWindow.find(".acrossTab li"),
        showTab = topWindow.find(".acrossTab li.active"),
        i = showTab.index();
    tab.eq(i - 1).addClass("active");
    tab.eq(i).remove();
    iframe.eq(i - 1).show();
    var ifms = iframe.find('iframe');
    if (ifms.length > 0) {
        if (ifms[i - 1]) {
            var cw = ifms[i - 1].contentWindow;
            if (cw.onTabSelected)
                cw.onTabSelected();
        }
    }
    num == 0 ? num = 0 : num--;
    tabNavallwidth();
    iframe.eq(i).remove();
}

/*关闭所有iframe*/
function removeIframeAll() {
    var topWindow = $(window.parent.document),
        iframe = topWindow.find('#iframe_box .show_iframe'),
        tab = topWindow.find(".acrossTab li");
    for (var i = 0; i < tab.length; i++) {
        if (tab.eq(i).find("i").length > 0) {
            tab.eq(i).remove();
            iframe.eq(i).remove();
        }
    }
}

/*弹出层*/

/*
 参数解释：
 title	标题
 url		请求的url
 id		需要操作的数据id
 w		弹出层宽度（缺省调默认值）
 h		弹出层高度（缺省调默认值）
 */
function layer_show(title, url, w, h) {
    if (title == null || title == '') {
        title = false;
    }
    ;
    if (url == null || url == '') {
        url = "404.html";
    }
    ;
    if (w == null || w == '') {
        w = 800;
    }
    ;
    if (h == null || h == '') {
        h = ($(window).height() - 50);
    }
    ;
    layer.open({
        type: 2,
        area: [w + 'px', h + 'px'],
        fix: false, //不固定
        maxmin: true,
        shade: 0.4,
        title: title,
        content: url
    });
}

/*关闭弹出框口*/
function layer_close() {
    var index = parent.layer.getFrameIndex(window.name);
    parent.layer.close(index);
}

/*时间*/
function getHTMLDate(obj) {
    var d = new Date();
    var weekday = new Array(7);
    var _mm = "";
    var _dd = "";
    var _ww = "";
    weekday[0] = "星期日";
    weekday[1] = "星期一";
    weekday[2] = "星期二";
    weekday[3] = "星期三";
    weekday[4] = "星期四";
    weekday[5] = "星期五";
    weekday[6] = "星期六";
    _yy = d.getFullYear();
    _mm = d.getMonth() + 1;
    _dd = d.getDate();
    _ww = weekday[d.getDay()];
    obj.html(_yy + "年" + _mm + "月" + _dd + "日 " + _ww);
};

$(function () {
    getHTMLDate($("#top_time"));
    getskincookie();
    //layer.config({extend: 'extend/layer.ext.js'});
    Huiasidedisplay();
    var resizeID;
    $(window).resize(function () {
        clearTimeout(resizeID);
        resizeID = setTimeout(function () {
            Huiasidedisplay();
        }, 500);
    });

    $(".nav-toggle").click(function () {
        $(".Hui-aside").slideToggle();
    });
    $(".Hui-aside").on("click", ".menu_dropdown dd li a", function () {
        if ($(window).width() < 768) {
            $(".Hui-aside").slideToggle();
        }
    });
    /*左侧菜单*/
    $.Huifold(".menu_dropdown dl dt", ".menu_dropdown dl dd", "fast", 1, "click");

    /*选项卡导航*/
    $(".Hui-aside").on("click", ".menu_dropdown a", function () {
        Hui_admin_tab(this);
    });

    /**
     *         var ifms = iframe_box.find('.show_iframe').find('iframe');
     if (ifms.length > 0) {
            if (ifms[bStopIndex]) {
                var cw = ifms[bStopIndex].contentWindow;
                if (cw.onTabSelected)
                    cw.onTabSelected();
            }

        }
     */

    $(document).on("click", "#min_title_list li i", function () {
        var aCloseIndex = $(this).parents("li").index();
        $(this).parent().remove();
        $('#iframe_box').find('.show_iframe').eq(aCloseIndex).remove();
        if (showIndex >= oUl.find('li').length) {
            showIndex = showIndex - 1;
        }
        show_frame_by_index(showIndex);
    });

    function show_frame_by_index(index) {
        showIndex = index;
        var iframe_box = $("#iframe_box");
        $("#min_title_list li").removeClass("active").eq(index).addClass("active");
        iframe_box.find(".show_iframe").hide().eq(index).show();
        var ifms = iframe_box.find('.show_iframe').find('iframe');
        if (ifms.length > 0) {
            if (ifms[index]) {
                var cw = ifms[index].contentWindow;
                if (cw.onTabSelected)
                    cw.onTabSelected();
            }
        }
        var $tabNavWp = $(window.parent.document).find(".Hui-tabNav-wp");
        if (oUl.width() > $tabNavWp.width()) {
            oUl.animate({'left': -(oUl.width() - $tabNavWp.width())}, 100);
        }
        num == 0 ? num = 0 : num--;
        tabNavallwidth();
    }

    $(document).on("click", "#min_title_list li span", function () {
        var bStopIndex = $(this).parents("li").index();
        show_frame_by_index(bStopIndex);
    });

    $(document).on("dblclick", "#min_title_list li", function () {
        var aCloseIndex = $(this).index();
        var iframe_box = $("#iframe_box");
        if (aCloseIndex > 0) {
            $(this).remove();
            $('#iframe_box').find('.show_iframe').eq(aCloseIndex).remove();
            if (showIndex >= oUl.find('li').length) {
                showIndex = showIndex - 1;
            }
            show_frame_by_index(showIndex);
        } else {
            return false;
        }
    });
    tabNavallwidth();

    $(window).resize(function () {
        num == 0 ? num = 0 : num--;
        toNavPos();
    });

    $('#js-tabNav-next').click(function () {
        num == oUl.find('li').length - 1 ? num = oUl.find('li').length - 1 : num++;
        toNavPos();
    });
    $('#js-tabNav-prev').click(function () {
        num == 0 ? num = 0 : num--;
        toNavPos();
    });

    function toNavPos() {
        oUl.stop().animate({'left': -num * 100}, 100);
    }

    /*换肤*/
    $("#Hui-skin .dropDown-menu a").click(function () {
        var v = $(this).attr("data-val");
        $.cookie("Huiskin", v);
        var hrefStr = $("#skin").attr("href");
        var hrefRes = hrefStr.substring(0, hrefStr.lastIndexOf('skin/')) + 'skin/' + v + '/skin.css';
        $(window.frames.document).contents().find("#skin").attr("href", hrefRes);
    });
});
