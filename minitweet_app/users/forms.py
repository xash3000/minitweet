from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField
from wtforms.validators import Length


class ProfileSettings(Form):
    website = StringField("website", validators=[Length(max=250)])
    bio = TextAreaField("bio", validators=[Length(max=250)])
