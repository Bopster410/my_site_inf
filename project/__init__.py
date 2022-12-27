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
login_manager.login_view = 'log_in'
login_manager.login_message_category = 'info'

from project import routes