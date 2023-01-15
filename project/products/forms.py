from project import db
from project.models import Product
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, ValidationError, IntegerField, TextAreaField
from wtforms.validators import Length, DataRequired

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