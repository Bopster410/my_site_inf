from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import Length, DataRequired, EqualTo, InputRequired

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=6, max=20), DataRequired()]) # TODO valid symbols
    email = EmailField('E-mail', validators=[DataRequired()]) # TODO valid email maybe
    password = PasswordField('Password', validators=[Length(min=6, max=20), DataRequired()]) # TODO valid symbols
    confirm_password = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password')])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign Up')