from . import main
from flask import render_template, url_for
from flask_login import current_user
from ..shared.models import Post
from .. import app, db


@main.route("/")  # pragma: no cover
@main.route("/posts")  # pragma: no cover
@main.route("/posts/newest/<int:page>")  # pragma: no cover
def home(page=1):
    """
    Main Page
    if the user is logged in show the posts from followed people
    else show all posts

    param: page -> for pagination
    example urls:
        /   (page=1)     # default
        /posts  (page=1)    # default
        /posts/newest/<page>    (page=page)
    """
    if current_user.is_authenticated and current_user.confirmed:
        # get posts from followed people
        posts = current_user.get_posts_from_followed_users()
    else:
        # query all posts in desceding order
        posts = Post.query.order_by(Post.id.desc())
    per_page = app.config["POSTS_PER_PAGE"]
    paginated_posts = posts.paginate(page, per_page)
    next_url = url_for("main.home", page=page + 1)
    prev_url = url_for("main.home", page=page - 1)
    return render_template("index.html",
                           posts=paginated_posts,
                           title="newest",
                           next_url=next_url,
                           prev_url=prev_url
                           )
