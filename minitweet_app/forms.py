from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField, PasswordField
from wtforms.validators import DataRequired


class PublishForm(Form):
    post_title = StringField('post_title', validators=[DataRequired()])
    textarea = TextAreaField("textarea", validators=[DataRequired()])


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class SignUpForm(Form):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
