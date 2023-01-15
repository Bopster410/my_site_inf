from project import db
from project.products.forms import AddProductForm, DeleteProductForm
from project.utils import save_image
from project.models import Product
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import current_user, login_required

products = Blueprint('products', __name__)

@products.route('/catalog')
def catalog():
    page = request.args.get('page', 1, type=int)
    products = db.paginate(db.select(Product), per_page=3, page=page)
    product_to_cart = db.session.execute(db.select(Product).where(Product.id == request.args.get('product_id'))).scalars().first()
    if product_to_cart:
        product_to_cart.owner = current_user
        db.session.commit()
    return render_template('catalog.html', products=products, with_navbar=True)


@products.route('/catalog/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.username == 'admin':
        form = AddProductForm()
        if form.validate_on_submit():
            image_file = save_image(form.image.data, 'products')
            product = Product(title=form.title.data, description=form.description.data, price=form.price.data, image=image_file)
            db.session.add(product)
            db.session.commit()
            flash('New product added successfully!', 'success')
            return redirect(url_for('products.add_product'))
        return render_template('add_product.html', form=form, with_navbar=True)
    else:
        return redirect(url_for('main.main_page'))

@products.route('/catalog/delete', methods=['GET', 'POST'])
@login_required
def delete_product():
    if current_user.username == 'admin':
        form = DeleteProductForm()
        if form.validate_on_submit():
            title = form.title_to_delete.data
            product_to_delete = db.session.execute(db.select(Product).where(Product.title == title)).scalars().first()
            db.session.delete(product_to_delete)
            db.session.commit()
            return redirect(url_for('products.delete_product'))
        return render_template('delete_product.html', form=form, with_navbar=True)
    else:
        return redirect(url_for('main.main_page'))

@products.route('/cart')
@login_required
def cart():
    return render_template('cart.html', with_navbar=True)