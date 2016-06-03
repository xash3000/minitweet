from flask_wtf import Form
from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired, Length


class PublishForm(Form):
    post_title = StringField('post_title',
                             validators=[DataRequired(), Length(min=5, max=50)]
                             )
    textarea = TextAreaField("textarea",
                             validators=[DataRequired(),
                                         Length(min=5, max=400)
                                         ]
                             )
