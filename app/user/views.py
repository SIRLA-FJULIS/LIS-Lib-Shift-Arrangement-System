from flask import render_template, redirect, url_for, request, session, abort
from app.user.forms import ContactForm, ReserveForm
from app.user import bp
from calendar import Calendar
from datetime import date, datetime
from app.models import ShiftArrangement
from app import db
from collections import defaultdict

@bp.route('/user')
def dashboard():
    return render_template('user/dashboard.html')

@bp.route('/book', methods = ['GET', 'POST'])
def book():
    cal = Calendar(0)
    today = date.today()
    cal_list = [[cal.monthdatescalendar(today.year+j, i+1) for i in range(12)] for j in range(2)]
    arrangements = ShiftArrangement.query.all()
    bookin_list = defaultdict(list)
    for arrangement in arrangements:
        bookin_list[str(arrangement.date)].append(arrangement.did)
    
    form = ReserveForm()
    if form.validate_on_submit():
        user_id = session['user_id']
        reserve_date = (int(form.year.data), int(form.month.data), int(form.day.data))
        duty_id = form.period.data
        form.period.data = ''

        exist_arrangements = ShiftArrangement.query.filter_by(date=date(*reserve_date)).all()
        if (exist_arrangements is None) or \
           (exist_arrangements is not None and duty_id not in [arr.did for arr in exist_arrangements]):
            db.session.add(ShiftArrangement(date=datetime(*reserve_date), uid=user_id, did=duty_id))
            db.session.commit()
        else:
            abort(500)
        return redirect(url_for('user.book'))
    return render_template('user/book.html', today=today, cal=cal_list, form=form, bookin_list=bookin_list)

@bp.route('/contact', methods = ['GET', 'POST'])
def contact():
    form = ContactForm()
    return render_template('user/contact.html', form=form)

@bp.route('/bookin_status', methods = ['GET'])
def get_bookin_status():
    year, month, day = request.args.get('date').split('-')
    query_date = f'{year.zfill(4)}-{month.zfill(2)}-{day.zfill(2)}'
    arrgements = ShiftArrangement.query.filter_by(date=query_date).all()
    bookin = [str(arr.did) for arr in arrgements]
    return " ".join(bookin)