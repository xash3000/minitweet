$(document).ready(function() {

    $(".heart").click(function() {
            var original = +$(this).parent().find(".likes-counting").html();
            if($(this).hasClass("fa-heart-o")){
                $(this).removeClass("fa-heart-o");
                $(this).addClass("fa-heart fa-3x");
                $(this).parent().find(".likes-counting").html(original + 1);
            } else {
                $(this).removeClass("fa-heart fa-3x");
                $(this).addClass("fa-heart-o");
                $(this).parent().find(".likes-counting").html(original - 1);
            }
    })
})
