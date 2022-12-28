from project import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalars().first()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    image = db.Column(db.String(20)) # TODO default and nullable
    password = db.Column(db.String(20), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='shawarma1.png') # TODO default and nullable
    price = db.Column(db.Integer, nullable=False)
    comments = db.relationship('Comment', backref='product', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(100), nullable=False)