from project import app, db
from project.forms import RegistrationForm
from project.models import User
from flask import render_template

@app.route('/reg', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    username = form.username.data
    password = form.password.data
    if username:
        db.session.add(User(username=username,  password=password))
        db.session.commit()
    return render_template('registration.html', form=form)

@app.route('/')
def main_page():
    return render_template('template.html')