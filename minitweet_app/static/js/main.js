$(document).ready(function() {

    $(".heart").click(function() {
            if($(this).hasClass("fa-heart-o")){
                $(this).removeClass("fa-heart-o");
                $(this).addClass("fa-heart fa-3x");
            } else {
                $(this).removeClass("fa-heart fa-3x");
                $(this).addClass("fa-heart-o");
            }
    })
})
