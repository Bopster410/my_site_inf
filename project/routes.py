from project import app, db, bcrypt
from project.forms import RegistrationForm, LogInForm, CommentForm, UpdateAccountForm
from project.models import User, Product, Comment
from flask import render_template, redirect, url_for, flash, request
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
            # next_page exists if user gets redirected
            # trying to get to the profile page being logged out
            next_page = request.args.get('next')
            # user will be forwarded to this next_page authentication
            return redirect(next_page if next_page else url_for('main_page')) 
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
    form = UpdateAccountForm()
    image_file = url_for('static', filename='profile_pics/' + current_user.image)
    return render_template('account.html', image_file=image_file, form=form, with_navbar=True)

@app.route('/catalog')
def catalog():
    page = request.args.get('page', 1, type=int)
    products = db.paginate(db.select(Product), per_page=2, page=page)
    # TODO if no products exist then another page
    return render_template('catalog.html', products=products, with_navbar=True)

@app.route('/comment', methods=['POST', 'GET'])
@login_required
def comment():
    form = CommentForm()
    prod_id = request.args.get('prod_id', type=int)
    product = db.session.execute(db.select(Product).where(Product.id == prod_id)).scalars().first()
    if form.validate_on_submit():
        comment = Comment(rate=form.rate.data, text=form.text.data, product=product)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('catalog'))
    return render_template('comment.html', form=form, product=product, with_navbar=True)

@app.route('/')
def main_page():
    return render_template('main_page.html', with_navbar=True)