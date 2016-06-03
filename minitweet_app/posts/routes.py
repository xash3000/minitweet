from . import posts
from flask import url_for, render_template, redirect, flash, jsonify
from sqlalchemy.sql.expression import func
from ..shared.models import Post, likes, User
from .forms import PublishForm
from flask_login import login_required, current_user
from ..shared.decorators import check_confirmed
from .. import app, db


@posts.route("/posts/discover/<int:page>")  # pragma: no cover
def discover(page=1):
    """
    show posts in random order
    example urls:
        /posts/discover  (page=1)    # default
        /posts/discover/<page>  (page=page)
    """
    _posts = Post.query.order_by(func.random())
    per_page = app.config["POSTS_PER_PAGE"]
    paginated_posts = _posts.paginate(page, per_page)
    next_url = url_for("posts.discover", page=page + 1)
    prev_url = url_for("posts.discover", page=page - 1)
    return render_template("index.html",
                           posts=paginated_posts,
                           title="discover",
                           next_url=next_url,
                           prev_url=prev_url
                           )


@posts.route("/posts/top/<int:page>")  # pragma: no cover
def top(page=1):
    """
    show the posts orderd by likes
    example urls:
        /posts/top  (page=1)    # default
        /posts/top/<page>  (page=page)
    """
    _posts = Post.query.join(likes).group_by(Post). \
        order_by(func.count(likes.c.post_id).desc())
    per_page = app.config["POSTS_PER_PAGE"]
    paginated_posts = _posts.paginate(page, per_page)
    next_url = url_for("posts.top", page=page + 1)
    prev_url = url_for("posts.top", page=page - 1)
    return render_template("index.html",
                           posts=paginated_posts,
                           title="top",
                           next_url=next_url,
                           prev_url=prev_url
                           )


@posts.route("/publish", methods=["GET", "POST"])  # pragma: no cover
@login_required  # pragma: no cover
@check_confirmed  # pragma: no cover
def publish():
    form = PublishForm()
    # check if the form pass all validators in forms.py
    if form.validate_on_submit():
        # POST request
        title = form.post_title.data
        body = form.textarea.data
        user_id = current_user.id
        # add new post to the database
        db.session.add(Post(title, body, user_id))
        db.session.commit()
        flash('New entry was successfully posted Thanks', 'success')
        # redirect user to the main page
        return redirect(url_for("main.home"))
    else:
        # GET request
        return render_template("publish.html", form=form, title="publish")


@posts.route("/u/<username>")  # pragma: no cover
@posts.route("/u/<username>/posts/<int:page>")  # pragma: no cover
@check_confirmed  # pragma: no cover
def user_profile_posts(username, page=1):
    # query user from the database by username
    # if user doesn't exsist throw 404 error
    user = User.query.filter_by(name=username).first_or_404()
    posts = user.posts.order_by(Post.id.desc())
    per_page = app.config["POSTS_PER_PAGE"]
    paginated_posts = posts.paginate(page, per_page)
    next_url = url_for("posts.user_profile_posts",
                       page=page + 1,
                       username=user.name
                       )
    prev_url = url_for("posts.user_profile_posts",
                       page=page - 1,
                       username=user.name
                       )
    if current_user.is_authenticated and current_user.name == user.name:
        user_profile = True
    else:
        user_profile = False
    return render_template("user_profile_posts.html",
                           user=user,
                           user_profile=user_profile,
                           posts=paginated_posts,
                           title=user.name,
                           next_url=next_url,
                           prev_url=prev_url
                           )


@posts.route("/post/<int:post_id>/like", methods=["POST"])  # pragma: no cover
def like_post(post_id):
    """
    like a post
    the request will sent with ajax
    example returned json:
        status: either "good" or "error"
        like: if user like the post like = True else like = None
        msg: if there is alert msg="some alert" else msg=None
        category: category of the msg (warning, primary, success)
    """
    msg = None
    like = None
    category = None
    post = Post.query.get(post_id)
    if not current_user.is_authenticated:
        status = "error"
        msg = "Please Login or signup first"
        category = "warning"
    elif not current_user.confirmed:
        status = "error"
        msg = "Please confirm your email first"
        category = "warning"
    else:
        if current_user.is_liking(post):
            current_user.unlike(post)
            like = False
        else:
            current_user.like(post)
            like = True
        status = "good"
        db.session.add(current_user)
        db.session.commit()
    return jsonify({"status": status,
                    "msg": msg,
                    "category": category,
                    "like": like,
                    "likes_counting": post.likers.count()
                    })
