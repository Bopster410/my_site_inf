from project import app
from flask import render_template

@app.route('/')
def hello_page():
    return render_template('template.html')