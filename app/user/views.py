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
    id = None
    reserve_date = None
    period = None
    cal = Calendar(0)
    year = date.today().year
    cal_list = [[cal.monthdatescalendar(year+j, i+1) for i in range(12)] for j in range(2)]
    form = ReserveForm()
    if form.validate_on_submit():
        reserve_date = form.year.data + "-" + form.month.data + "-" + form.day.data
        print(reserve_date)
        period = form.period.data
        form.period.data = ''
        return redirect(url_for('user.book'))
    return render_template('user/book.html', today_year=year, cal=cal_list, form=form)
 
@bp.route('/contact', methods = ['GET', 'POST'])
def contact():
    form = ContactForm()
    return render_template('user/contact.html', form=form)