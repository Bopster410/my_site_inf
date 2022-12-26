from project import db
from project.models import User
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Length, DataRequired, EqualTo, InputRequired

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=6, max=20), DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired()]) 
    password = PasswordField('Password', validators=[Length(min=6, max=20), DataRequired()]) # TODO valid symbols
    confirm_password = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign Up')

    def validate_username(form, field):
        exists = db.session.execute(db.select(User).where(User.username == field.data)).scalars().first() != None
        valid_symbols = re.match(r'[a-zA-Z][a-zA-Z0-9_]*', field.data) != None
        if exists:
            raise ValidationError('This username is already taken')
        elif not valid_symbols:
            raise ValidationError('Username is invalid')
    
    def validate_email(form, field):
        exists = db.session.execute(db.select(User).where(User.email == field.data)).scalars().first()
        if exists:
            raise ValidationError('This email is already taken')


class LogInForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    log_in = SubmitField('Log In')