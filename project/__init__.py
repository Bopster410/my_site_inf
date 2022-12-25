from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '76ab62945617c423e8b122cfffb9ac1a'

from project import routes