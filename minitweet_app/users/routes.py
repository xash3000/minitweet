from flask import jsonify, abort, flash, redirect, url_for
from . import users
from .. import bcrypt, db
from ..shared.decorators import check_confirmed
from ..shared.models import User
from flask import render_template
from flask_login import login_required, current_user
from .forms import ProfileSettings


@users.route('/u/<username>/following')  # pragma: no cover
@check_confirmed  # pragma: no cover
def following(username):
    user = User.query.filter_by(name=username).first_or_404()
    if current_user.is_authenticated and current_user.name == user.name:
        user_profile = True
    else:
        user_profile = False
    users = user.following.all()
    return render_template("user_following_and_followers.html",
                           user=user,
                           users=users,
                           user_profile=user_profile,
                           title="{} followings".format(user.name)
                           )


@users.route('/u/<username>/followers')  # pragma: no cover
@check_confirmed  # pragma: no cover
def followers(username):
    user = User.query.filter_by(name=username).first_or_404()
    if current_user.is_authenticated and current_user.name == user.name:
        user_profile = True
    else:
        user_profile = False
    users = user.followers.all()
    return render_template("user_following_and_followers.html",
                           user=user,
                           user_profile=user_profile,
                           users=users,
                           followers=True,
                           title="{} followers".format(user.name)
                           )


@users.route("/u/<username>/profile_settings", methods=["GET", "POST"]) \
    # pragma: no cover
def profile_settings(username):
    user = User.query.filter_by(name=username).first_or_404()
    form = ProfileSettings()
    if form.validate_on_submit():
        # POST request
        user.bio = form.bio.data
        user.website = form.website.data
        db.session.add(user)
        db.session.commit()
        flash("new settings were successfully applied", "success")
        view = "posts.user_profile_posts"
        return redirect(url_for(view, username=user.name))
    # GET request
    if current_user.is_authenticated and current_user.name == user.name:
        form.website.data = current_user.website
        form.bio.data = current_user.bio
        return render_template("profile_settings.html",
                               form=form,
                               user_bio=user.bio,
                               title="profile settings"
                               )
    else:
        return abort(403)


@users.route("/u/<username>/follow_or_unfollow", methods=["POST"]) \
    # pragma: no cover
def follow_or_unfollow(username):
    """
    follow_or_unfollow user
    the request will sent with ajax
    example returned json:
        status: either "good" or "error"
        follow: if user follow the user follow = True else follow = None
        msg: if there is alert msg="some alert" else msg=None
        category: category of the msg (warning, primary, success)
    """
    msg = None
    category = None
    follow = False
    user = User.query.filter_by(name=username).first_or_404()
    if not current_user.is_authenticated:
        status = "error"
        msg = "Please Login or signup first"
        category = "warning"
    elif not current_user.confirmed:
        status = "error"
        msg = "Please confirm your email first"
        category = "warning"
    else:
        status = "good"
        if not current_user.is_following(user):
            follow = True
            current_user.follow(user)
        elif current_user.is_following(user):
            current_user.unfollow(user)
        db.session.add(current_user)
        db.session.commit()
    return jsonify({"status": status,
                    "msg": msg,
                    "category": category,
                    "follow": follow
                    })


@users.route("/discover_users")  # pragma: no cover
@login_required  # pragma: no cover
@check_confirmed  # pragma: no cover
def discover_users():
    users = User.query.all()
    return render_template("discover_users.html", users=users)
