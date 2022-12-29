from project import db
from project.models import User, Product
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField, ValidationError, IntegerField, TextAreaField
from wtforms.validators import Length, DataRequired, EqualTo, InputRequired
from flask_login import current_user
import re

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=6, max=20), DataRequired()])
    email = EmailField('Email', validators=[DataRequired()]) 
    password = PasswordField('Password', validators=[Length(min=6, max=20), DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
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
    remember_me = BooleanField('Remember me')
    log_in = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=6, max=20), DataRequired()])
    email = EmailField('Email', validators=[DataRequired()]) 
    image = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_username(form, field):
        if field.data != current_user.username:
            exists = db.session.execute(db.select(User).where(User.username == field.data)).scalars().first() != None
            valid_symbols = re.match(r'[a-zA-Z][a-zA-Z0-9_]*', field.data) != None
            if exists:
                raise ValidationError('This username is already taken')
            elif not valid_symbols:
                raise ValidationError('Username is invalid')
    
    def validate_email(form, field):
        if field.data != current_user.email:
            exists = db.session.execute(db.select(User).where(User.email == field.data)).scalars().first()
            if exists:
                raise ValidationError('This email is already taken')


class CommentForm(FlaskForm):
    text = TextAreaField('Comment text', validators=[DataRequired(), Length(min=1, max=100)])
    rate = IntegerField('Rate')
    submit = SubmitField('Submit')


class AddProductForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=6, max=20), DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=6, max=100), DataRequired()]) 
    price = IntegerField('Price', validators=[DataRequired()])
    image = FileField('Product picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

    def validate_title(form, field):
        exists = db.session.execute(db.select(Product).where(Product.title == field.data)).scalars().first() != None
        if exists:
            raise ValidationError('This title is already exists')

    def validate_price(form, field):
        if field.data <= 0:
            raise ValidationError('Price must be greater than 0')


class DeleteProductForm(FlaskForm):
    title_to_delete = StringField('Title', validators=[DataRequired(), Length(min=6, max=20)])
    delete = SubmitField('Delete')

    def validate_title_to_delete(form, field):
        exists = db.session.execute(db.select(Product).where(Product.title == field.data)).scalars().first() != None
        if not exists:
            raise ValidationError("This title doesn't exist")