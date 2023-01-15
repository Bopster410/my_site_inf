from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, TextAreaField
from wtforms.validators import Length, DataRequired

class CommentForm(FlaskForm):
    text = TextAreaField('Comment text', validators=[DataRequired(), Length(min=1, max=100)])
    rate = IntegerField('Rate')
    submit = SubmitField('Submit')
