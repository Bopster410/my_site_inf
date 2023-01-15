from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proj.db'
app.config['SECRET_KEY'] = '76ab62945617c423e8b122cfffb9ac1a'
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = 'users.log_in'
login_manager.login_message_category = 'info'

from project.users.routes import users
app.register_blueprint(users)

from project.products.routes import products
app.register_blueprint(products)

from project.comments.routes import comments
app.register_blueprint(comments)

from project.main.routes import main
app.register_blueprint(main)