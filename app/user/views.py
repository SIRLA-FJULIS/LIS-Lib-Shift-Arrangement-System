from flask import render_template, redirect, url_for
from app.user.forms import ContactForm, ReserveForm
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
    return render_template('user/contact.html', form=form)

@bp.route('/reserve', methods = ['GET', 'POST'])
def reserve():
    id = None
    date = None
    period = None
    form = ReserveForm()
    if form.validate_on_submit():
        id = form.id.data
        form.id.data = ''
        date = form.date.data
        form.date.data = ''
        period = form.period.data
        form.period.data = ''
    return render_template('user/reserve.html', form=form)