# flask imports
from flask import render_template, redirect, url_for, request, flash, abort

#flask.extensions imports
from flask.ext.login import (
    login_user, login_required, logout_user, current_user
)

# in package imports
from .forms import PublishForm, SignUpForm, LoginForm
from . import app, db, bcrypt
from .models import Post, User


@app.route("/")
@app.route("/posts")
def home():
    """ Main Page """
    # query all posts in desceding order
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template("index.html", posts=posts)


@app.route("/publish", methods=["GET", "POST"])
@login_required
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
        flash('New entry was successfully posted. Thanks.', 'success')
        # redirect user to the main page
        return redirect(url_for("home"))
    else:
        # GET request
        return render_template("publish.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # POST request
        # query user from the database by username
        user = User.query.filter(User.name == form.username.data).first()
        # check if user exsist and the password match the hash stored in the database
        if user and bcrypt.check_password_hash(user.password, form.password.data):
                flash("you were just logged in!", 'success')
                remember = form.remember_me.data
                login_user(user, remember=remember)
                return redirect(url_for("home"))
        else:
            # invalid inputs
            flash("Invalid username or password", 'danger')
    # GET request
    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # POST request
        # create new User instance
        u = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        # add new user to the database
        db.session.add(u)
        db.session.commit()
        # login user
        login_user(u, remember=True)
        return redirect(url_for('home'))
    # GET request
    return render_template("signup.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("you were just logged out!", 'success')
    return redirect(url_for("home"))


@app.route("/u/<username>")
def user_profile(username):
    # query user from the database by username
    # if user doesn't exsist throw 404 error
    user = User.query.filter_by(name=username).first_or_404()
    return render_template(
            "user_profile.html",
            user=user,
        )
