from flask_wtf import FlaskForm
from wtforms import  StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required

class PitchForm(FlaskForm):
    content = TextAreaField('Pitch')
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment_id = TextAreaField('Comment')
    submit = SubmitField('Submit') 