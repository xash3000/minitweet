$(document).ready(function() {

    function createAlert(msg, category) {
        var message = $("<div>", {class: "message flashed-alert col-xs-12", display: "inline-block"});
        var div = $("<div>", {style:"padding: 5px;"});
        var _alert = $('<div>', {class: "alert alert-" + category +" text-center"});
        var a = $("<a>", {class: "close", title: "Close", href: "#", dataDismiss:"alert"}).text('×');
        var span = $("<span>", {class: "msg"}).text(msg);

        $("body").append(message);
        message.append(div);
        div.append(_alert);
        _alert.append(a);
        _alert.append(span);
        setTimeout(function() {
            message.fadeOut('slow');
        }, 3000)
    }

    $('.close').click(function() {
        $(this).closest(".message").fadeOut()
    })

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
                    if (data.status === "good"){
                        if(data.like){
                            heart.addClass("fa-heart fa-3x")
                        } else {
                            heart.addClass("fa-heart-o fa-2x")
                        }
                        heart.next().text(data.likes_counting)
                    } else if (data.status === "error") {
                        heart.addClass("fa-heart-o fa-2x");
                        createAlert(data.msg, data.category);
                    }
                }, "json")
    })

    $('.follow-btn').click(function() {
        var followBtn = $(this)
        followBtn.removeClass("btn btn-success btn-danger").addClass('fa fa-3x fa-spinner fa-spin disabled');
        followBtn.text(null)
        var username = followBtn.parent().data("username");
        $.post(
            // var root defined in templates/base.html
            root + "/u/" + username + "/follow_or_unfollow",
            function(data) {
                followBtn.removeClass('fa fa-3x fa-spinner fa-spin disabled')
                if (data.status === "good") {
                    if (data.follow === true){
                        followBtn.addClass("btn btn-danger")
                        followBtn.text("Unfollow")
                    } else if (data.follow === false) {
                        followBtn.addClass("btn btn-success")
                        followBtn.text("Follow")
                    }
                } else if (data.status === "error") {
                    followBtn.addClass("btn btn-success follow-btn");
                    createAlert(data.msg, data.category);
                }
            }
        )
    })

    $('.flashed-alert').ready(function() {
        setTimeout(function() {
            $(".flashed-alert").fadeOut('slow');
        }, 3000)
    })
})
