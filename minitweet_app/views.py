# flask imports
from flask import render_template, redirect, url_for, request, flash

#flask.ext
from flask.ext.login import (
    login_user, login_required, logout_user, current_user
)

# in package import
from .forms import PublishForm, SignUpForm, LoginForm
from . import app, db, load_user
from .models import Post, User

@app.route("/")
@app.route("/posts")
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template("index.html", posts=posts)


@app.route("/publish", methods=["GET", "POST"])
@login_required
def publish():
    form = PublishForm()
    if form.validate_on_submit():
        title = form.post_title.data
        body = form.textarea.data
        user_id = current_user.id
        db.session.add(Post(title, body, user_id))
        db.session.commit()
        flash('New entry was successfully posted. Thanks.')
        return redirect(url_for("home"))
    else:
        return render_template("publish.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.name == form.username.data).first()
        if user and user.password == form.password.data:
            flash("you were just logged in!")
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("bad username or password")
    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template("signup.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("you were just logged out!")
    return redirect(url_for("home"))
