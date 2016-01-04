# flask imports
from flask import render_template, redirect, url_for, request, flash, abort

#flask.ext
from flask.ext.login import (
    login_user, login_required, logout_user, current_user
)

# in package import
from .forms import PublishForm, SignUpForm, LoginForm
from . import app, db, load_user, bcrypt
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
        if user and bcrypt.check_password_hash(user.password, form.password.data):
                flash("you were just logged in!")
                remember = form.remember_me.data
                login_user(user, remember=remember)
                return redirect(url_for("home"))
        else:
            flash("Invalid username or password")
    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        u = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(u)
        db.session.commit()
        u.id = int(u.id)
        login_user(u, remember=True)
        return redirect(url_for('home'))
    return render_template("signup.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("you were just logged out!")
    return redirect(url_for("home"))


@app.route("/u/<username>")
def user_profile(username):
    user = User.query.filter_by(name=username).first_or_404()
    return render_template(
            "user_profile.html",
            user=user,
        )
