from flask import render_template
from app.user.forms import ContactForm
from app.user import bp
from calendar import Calendar
from datetime import date

@bp.route('/dashboard')
def dashboard():
    return render_template('user/dashboard.html')

@bp.route('/book', methods = ['GET', 'POST'])
def book():
    cal = Calendar(0)
    year = date.today().year
    cal_list = [cal.monthdatescalendar(year, i+1) for i in range(12)]
    return render_template('user/book.html', year=year, cal=cal_list)

@bp.route('/contact', methods = ['GET', 'POST'])
def contact():
    form = ContactForm()
    return render_template('user/contact.html', form = form)