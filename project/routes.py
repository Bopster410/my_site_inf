from project import app, db, bcrypt
from project.forms import RegistrationForm, LogInForm
from project.models import User
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/reg', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data)
        email = form.email.data
        db.session.add(User(username=username,  password=password, email=email))
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('log_in'))
    return render_template('registration.html', form=form)

@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    form = LogInForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalars().first()
        if user and  bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main_page'))
        else:
            flash('Check your email and password.', 'danger')
    return render_template('log_in.html', form=form)

@app.route('/log_out')
def log_out():
    logout_user()
    return redirect(url_for('main_page'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', with_navbar=True)

@app.route('/')
def main_page():
    return render_template('main_page.html', with_navbar=True)