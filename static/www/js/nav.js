$(function(){
    //导航
    var NavWaitSlide;
    $('#mynav > li').hover(
        function(){
            $(this).find('a:first').addClass("hover");
            var current_li=$(this),targ=$(current_li).find('ul:first');
            NavWaitSlide = setTimeout(function() {
                //if(!$(targ).is(':visible'))
                //{
                    $(targ).slideDown(100);
                //}
            },100)
        },
        function(){
            clearTimeout(NavWaitSlide);
            $(this).find('ul').hide(200);
            $(this).find('a:first').removeClass("hover");

        }
    );
    $(function(){
      $('.nav-detail').on('show.bs.collapse', function () {
         $(this).prev().children().removeClass("glyphicon-plus");
         $(this).prev().children().addClass("glyphicon-minus");
     })
      $('.nav-detail').on('hide.bs.collapse', function () {
         $(this).prev().children().removeClass("glyphicon-minus");
         $(this).prev().children().addClass("glyphicon-plus");
     })
});
})