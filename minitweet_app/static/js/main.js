$(document).ready(function() {
    $(".heart").click(function() {
            var heart = $(this)
            heart.removeClass("fa-heart-o fa-heart");
            heart.addClass("fa-spinner fa-spin disabled");
            var postId = heart.closest('.post')[0].id;
            $.post(
                // var root defined in templates/base.html
                root + "/post/" + postId + "/like",
                function(data) {
                    heart.removeClass("fa-spinner fa-spin fa-heart-o fa-heart disabled fa-3x fa-2x");
                    if(data.like){
                        heart.addClass("fa-heart fa-3x")
                    } else {
                        heart.addClass("fa-heart-o fa-2x")
                    }
                    heart.next().text(data.likes_counting)
                }, "json")
    })

    setTimeout(function() {
            $(".flashed-alert").fadeOut('slow');
    }, 3000)

})
