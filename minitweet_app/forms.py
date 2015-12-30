from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired

class Publish(Form):
    username = StringField('username', validators=[DataRequired()])
    post_title = StringField('post-title', validators=[DataRequired()])
    textarea = TextAreaField("textarea", validators=[DataRequired()])
