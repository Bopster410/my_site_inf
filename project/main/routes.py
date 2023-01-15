from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def main_page():
    return render_template('main_page.html', with_navbar=True)