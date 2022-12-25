from project import app
from project.forms import RegistrationForm
from flask import render_template

@app.route('/reg')
def registration():
    form = RegistrationForm()
    return render_template('registration.html', form=form)

@app.route('/')
def main_page():
    return render_template('template.html')