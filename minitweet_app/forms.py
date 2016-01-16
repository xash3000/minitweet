from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class PublishForm(Form):
    post_title = StringField(
            'post_title', validators=[DataRequired(), Length(min=5, max=50)]
    )
    textarea = TextAreaField(
            "textarea", validators=[DataRequired(), Length(min=5, max=400)]
    )


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField("remember_me", default=True)


class SignUpForm(Form):
    username = StringField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        'email',
        validators=[DataRequired(), Email(), Length(min=5)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6)]
    )


class ProfileSettings(Form):
    website = StringField("website", validators=[Length(max=250)])
    bio = TextAreaField("bio", validators=[Length(max=250)])
