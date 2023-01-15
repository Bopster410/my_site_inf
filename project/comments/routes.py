from project import db
from project.comments.forms import CommentForm
from project.models import Product, Comment
from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import current_user, login_required

comments = Blueprint('comments', __name__)

@comments.route('/comment', methods=['POST', 'GET'])
@login_required
def comment():
    form = CommentForm()
    prod_id = request.args.get('prod_id', type=int)
    product = db.session.execute(db.select(Product).where(Product.id == prod_id)).scalars().first()
    if form.validate_on_submit():
        comment = Comment(rate=form.rate.data, text=form.text.data, product=product, author=current_user)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('products.catalog'))
    return render_template('comment.html', form=form, product=product, with_navbar=True)
