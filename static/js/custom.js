/**
 * Created by stone on 2017/7/7.
 */
+function (B, $) {

    B.showHuiDialog = function (title, msg, callback) {
        layer.confirm(msg, {
            title:title,
            btn: ['确认', '取消'] //按钮
        }, function () {
            if(typeof(callback) == 'function'){
                callback();
            }
        }, function () {

        });
        // $.HuiDialogBox.Confirm(title,msg,ok);
    }

}(IR, jQuery);

B = Base = IR;

