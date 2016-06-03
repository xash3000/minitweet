from flask import render_template, flash, redirect, url_for
from . import auth
from flask_login import login_required, login_user, logout_user, current_user
from ..shared.models import User
from .forms import LoginForm, SignUpForm
from ..shared.decorators import check_user_already_logged_in
from .. import bcrypt, db
from .confirmation_token import confirm_token, generate_confirmation_token
from .email import send_email


@auth.route("/login", methods=["GET", "POST"])  # pragma: no cover
@check_user_already_logged_in  # pragma: no cover
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # POST request
        # query user from the database by username
        user = User.query.filter(User.name == form.username.data).first()
        # check if user exsist and the password match the hash in the database
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
                flash("you were just logged in", 'success')
                remember = form.remember_me.data
                login_user(user, remember=remember)
                return redirect(url_for("main.home"))
        else:
            # invalid inputs
            flash("Invalid username or password", 'danger')
    # GET request
    return render_template("login.html", form=form, title="Login")


@auth.route("/signup", methods=["GET", "POST"])  # pragma: no cover
@check_user_already_logged_in  # pragma: no cover
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # POST request
        check_u = User.query.filter_by(email=form.email.data).first()
        if check_u:
            if check_u.email == form.email.data:
                flash('email already exsist', "danger")
                return redirect(url_for('auth.signup'))
        check_u2 = User.query.filter_by(name=form.username.data).first()
        if check_u2:
            if check_u2.name == form.username.data:
                flash('username already exsist', "danger")
                return redirect(url_for('auth.signup'))
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


@auth.route('/logout')  # pragma: no cover
@login_required  # pragma: no cover
def logout():
    logout_user()
    flash("you were just logged out", 'success')
    return redirect(url_for("main.home"))


@auth.route('/confirm/<token>')  # pragma: no cover
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
    return redirect(url_for('users.discover_users'))


@auth.route("/unconfirmed")  # pragma: no cover
@login_required  # pragma: no cover
def unconfirmed():
    if current_user.confirmed or not current_user.is_authenticated:
        return redirect(url_for('main.home', page=1))
    flash('Please confirm your account', 'warning')
    return render_template('unconfirmed.html', title="unconfirmed")


@auth.route('/resend_confirmation')  # pragma: no cover
@login_required  # pragma: no cover
def resend_confirmation():
    """
    resend email confirmation to user
    """
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('email_activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent', 'success')
    return redirect(url_for('auth.unconfirmed'))
