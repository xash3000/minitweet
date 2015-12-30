from flask import render_template, redirect, url_for, request
from .forms import Publish
from . import app, db
from .models import Post

@app.route("/")
@app.route("/posts")
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template("index.html", posts=posts)


@app.route("/publish", methods=["GET", "POST"])
def publish():
    form = Publish()
    if form.validate_on_submit():
        title = form.post_title.data
        author = form.username.data
        body = form.textarea.data
        db.session.add(Post(title, author, body))
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("publish.html", form=form)
