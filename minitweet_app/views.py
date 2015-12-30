from flask import render_template, redirect, url_for, request, flash
from .forms import PublishForm, SignUpForm, LoginForm
from . import app, db
from .models import Post

@app.route("/")
@app.route("/posts")
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template("index.html", posts=posts)


@app.route("/publish", methods=["GET", "POST"])
def publish():
    form = PublishForm()
    if form.validate_on_submit():
        #title = form.post_title.data
        #body = form.textarea.data
        #db.session.add(Post(title, body))
        #db.session.commit()
        return redirect(url_for("home"))
    else:
        errors = form.errors.items()
        return render_template("publish.html", form=form, errors=errors)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        #db.session.add()
        #db.session.commit()
        return redirect(url_for("home"))
    else:
        errors = form.errors.items()
        return render_template("login.html", form=form, errors=errors)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():

        #db.session.add()
        #db.session.commit()
        return redirect(url_for("home"))
    else:
        return render_template("signup.html", form=form)
