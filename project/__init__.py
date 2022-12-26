from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proj.db'
app.config['SECRET_KEY'] = '76ab62945617c423e8b122cfffb9ac1a'
db = SQLAlchemy(app)

from project import routes