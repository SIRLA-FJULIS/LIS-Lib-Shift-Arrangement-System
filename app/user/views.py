from flask import render_template
from app.user.forms import BookForm
from app.user import bp

@bp.route('/dashboard')
def dashboard():
    return render_template('user/dashboard.html')

@bp.route('/book', methods = ['GET', 'POST'])
def book():
    form = BookForm()
    return render_template('user/book.html', form = form)