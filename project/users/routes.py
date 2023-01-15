from project import db, bcrypt
from project.users.forms import RegistrationForm, LogInForm, UpdateAccountForm
from project.utils import save_image
from project.models import User, Product, Comment
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
import os

users = Blueprint('users', __name__)

@users.route('/reg', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data)
        email = form.email.data
        db.session.add(User(username=username,  password=password, email=email))
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('users.log_in'))
    return render_template('registration.html', form=form)

@users.route('/log_in', methods=['GET', 'POST'])
def log_in():
    form = LogInForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalars().first()
        if user and  bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            # next_page exists if user gets redirected
            # trying to get to the profile page being logged out
            next_page = request.args.get('next')
            # user will be forwarded to this next_page authentication
            return redirect(next_page if next_page else url_for('main.main_page')) 
        else:
            flash('Check your email and password.', 'danger')
    return render_template('log_in.html', form=form)

@users.route('/log_out')
def log_out():
    logout_user()
    return redirect(url_for('main.main_page'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            if current_user.image != 'default.jpg':
                os.remove(os.path.join(users.root_path, 'static/profile_pics', current_user.image))
            image_file = save_image(form.image.data, 'profile_pics')
            current_user.image = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account was updated successfully!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image)
    return render_template('account.html', image_file=image_file, form=form, with_navbar=True)
