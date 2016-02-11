# ``# pragma: no cover`` is to exclude lines from coverage test
# flask imports
from flask import render_template, redirect, url_for, request, flash, abort \
  # pragma: no cover

#flask.extensions imports
from flask.ext.login import (
    login_user, login_required, logout_user, current_user   # pragma: no cover
)
from  sqlalchemy.sql.expression import func

# in package imports
from .forms import PublishForm, SignUpForm, LoginForm, ProfileSettings   # pragma: no cover
from . import app, db, bcrypt  # pragma: no cover
from .models import Post, User  # pragma: no cover
from .confirmation_token import generate_confirmation_token, confirm_token  # pragma: no cover
from .email import send_email  # pragma: no cover
from .decorators import check_confirmed, check_user_already_logged_in  # pragma: no cover

import re


def redirect_back(default='home'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


@app.route("/")  # pragma: no cover
@app.route("/posts")  # pragma: no cover
@app.route("/posts/newest")  # pragma: no cover
def home():
    """ Main Page """
    # query all posts in desceding order
    if current_user.is_authenticated and current_user.confirmed:
        posts = current_user.get_posts_from_followed_users()
    else:
        posts = Post.query.order_by(Post.id.desc())
    return render_template("index.html", posts=posts, title="newest")


@app.route("/posts/discover")
def discover():
    posts = Post.query.order_by(func.random()).limit(20)
    return render_template("index.html", posts=posts, title="discover")


@app.route("/publish", methods=["GET", "POST"])  # pragma: no cover
@login_required  # pragma: no cover
@check_confirmed  # pragma: no cover
def publish():
    form = PublishForm()
    # check if the form pass all validators in forms.py
    if form.validate_on_submit():
        # POST request
        title = form.post_title.data
        body = re.sub(r'<[^>]*?>', '', form.textarea.data)
        user_id = current_user.id
        # add new post to the database
        db.session.add(Post(title, body, user_id))
        db.session.commit()
        flash('New entry was successfully posted Thanks', 'success')
        # redirect user to the main page
        return redirect(url_for("home"))
    else:
        # GET request
        return render_template("publish.html", form=form, title="publish")


@app.route("/login", methods=["GET", "POST"])  # pragma: no cover
@check_user_already_logged_in
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # POST request
        # query user from the database by username
        user = User.query.filter(User.name == form.username.data).first()
        # check if user exsist and the password match the hash stored in the database
        if user and bcrypt.check_password_hash(user.password, form.password.data):
                flash("you were just logged in", 'success')
                remember = form.remember_me.data
                login_user(user, remember=remember)
                return redirect(url_for("home"))
        else:
            # invalid inputs
            flash("Invalid username or password", 'danger')
    # GET request
    return render_template("login.html", form=form, title="Login")


@app.route("/signup", methods=["GET", "POST"])  # pragma: no cover
@check_user_already_logged_in
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # POST request
        check_u = User.query.filter_by(email=form.email.data).first()
        if check_u:
            if check_u.email == form.email.data:
                flash('email already exsist', "danger")
                return redirect(url_for('signup'))
        check_u2 = User.query.filter_by(name=form.username.data).first()
        if check_u2:
            if check_u2.name == form.username.data:
                flash('username already exsist', "danger")
                return redirect(url_for('signup'))
        # create new User instance
        u = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data,
            confirmed=False
        )
        # add new user to the database
        db.session.add(u)
        db.session.commit()
        token = generate_confirmation_token(u.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('email_activate.html', confirm_url=confirm_url)
        subject = "email confirmation for minitweet"
        send_email(u.email, subject, html)
        login_user(u)
        flash('A confirmation email has been sent via email', 'success')
        return redirect(url_for("unconfirmed"))

    # GET request
    return render_template("signup.html", form=form, title="signup")


@app.route('/logout')  # pragma: no cover
@login_required  # pragma: no cover
def logout():
    logout_user()
    flash("you were just logged out", 'success')
    return redirect(url_for("home"))


@app.route("/u/<username>")  # pragma: no cover
@app.route("/u/<username>/posts")  # pragma: no cover
@check_confirmed  # pragma: no cover
def user_profile_posts(username):
    # query user from the database by username
    # if user doesn't exsist throw 404 error
    user = User.query.filter_by(name=username).first_or_404()
    posts = user.posts.order_by(Post.id.desc())
    if current_user.is_authenticated and current_user.name == user.name:
        user_profile = True
    else:
        user_profile = False
    return render_template(
            "user_profile_posts.html",
            user=user,
            user_profile=user_profile,
            posts=posts,
            title=user.name
        )


@app.route('/u/<username>/following')  # pragma: no cover
@check_confirmed  # pragma: no cover
def following(username):
    user = User.query.filter_by(name=username).first_or_404()
    if current_user.is_authenticated and current_user.name == user.name:
        user_profile = True
    else:
        user_profile = False
    users = user.following.all()
    return render_template(
            "user_following_and_followers.html",
            user=user,
            users=users,
            user_profile=user_profile,
            title="{} followings".format(user.name)
        )


@app.route('/u/<username>/followers')  # pragma: no cover
@check_confirmed  # pragma: no cover
def followers(username):
    user = User.query.filter_by(name=username).first_or_404()
    if current_user.is_authenticated and current_user.name == user.name:
        user_profile = True
    else:
        user_profile = False
    users = user.followers.all()
    return render_template(
            "user_following_and_followers.html",
            user=user,
            user_profile=user_profile,
            users=users,
            followers=True,
            title="{} followers".format(user.name)
        )


@app.route("/u/<username>/profile_settings", methods=["GET", "POST"])  # pragma: no cover
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
        return redirect(url_for("user_profile_posts", username=user.name))
    # GET request
    if current_user.is_authenticated and current_user.name == user.name:
        return render_template("profile_settings.html",
                form=form,
                user_bio=user.bio,
                title="profile settings"
            )
    else:
        return abort(403)


@app.route('/confirm/<token>')  # pragma: no cover
def confirm_email(token):
    try:
        # try confirm_email
        email = confirm_token(token)
        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            flash('Account already confirmed Please login.', 'success')
        else:
            user.confirmed = True
            # user follow himself to show his posts in the main page
            user.follow(user)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('You have confirmed your account Thanks', 'success')
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('discover_users'))


@app.route("/unconfirmed")  # pragma: no cover
@login_required  # pragma: no cover
def unconfirmed():
    if current_user.confirmed or not current_user.is_authenticated:
        return redirect(url_for('home'))
    flash('Please confirm your account', 'warning')
    return render_template('unconfirmed.html', title="unconfirmed")


@app.route('/resend_confirmation')  # pragma: no cover
@login_required  # pragma: no cover
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('email_activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent', 'success')
    return redirect(url_for('unconfirmed'))


@app.route("/u/<username>/follow")  # pragma: no cover
@login_required  # pragma: no cover
@check_confirmed  # pragma: no cover
def follow(username):
    user = User.query.filter_by(name=username).first_or_404()
    if current_user.is_following(user):
        flash("you are already following {}".format(user.name), "primary")
        return redirect(redirect_back())
    else:
        current_user.follow(user)
        db.session.add(current_user)
        db.session.commit()
        flash("you successfully followed {}".format(user.name), "success")
        return redirect(redirect_back())


@app.route("/u/<username>/unfollow")  # pragma: no cover
@login_required  # pragma: no cover
@check_confirmed  # pragma: no cover
def unfollow(username):
    user = User.query.filter_by(name=username).first_or_404()
    if not current_user.is_following(user):
        flash('you are not following {}'.format(user.name), "primary")
        return redirect(redirect_back())
    else:
        current_user.unfollow(user)
        db.session.add(current_user)
        db.session.commit()
        flash("you successfully Unfollowed {}".format(user.name), "success")
        return redirect(redirect_back())


@app.route("/discover_users")  # pragma: no cover
@login_required  # pragma: no cover
@check_confirmed  # pragma: no cover
def discover_users():
    users = User.query.all()
    return render_template("discover_users.html", users=users)
