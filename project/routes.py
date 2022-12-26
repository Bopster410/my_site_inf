from project import app, db
from project.forms import RegistrationForm, LogInForm
from project.models import User
from flask import render_template, redirect, url_for

@app.route('/reg', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        db.session.add(User(username=username,  password=password, email=email))
        db.session.commit()
        redirect(url_for('main_page'))
    return render_template('registration.html', form=form)

@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    form = LogInForm()
    return render_template('log_in.html', form=form)

@app.route('/')
def main_page():
    return render_template('template.html')