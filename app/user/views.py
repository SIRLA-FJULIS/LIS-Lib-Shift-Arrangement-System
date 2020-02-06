from flask import render_template, redirect, url_for, request, session, abort
from app.user.forms import ContactForm, ReserveForm
from app.user import bp
from calendar import Calendar
from datetime import date, datetime, timedelta
from app.models import ShiftArrangement, Semester
from app import db
from collections import defaultdict

@bp.route('/user')
def dashboard():
    return render_template('user/dashboard.html')

def is_period_duplicate(reserve_date, duty_id):
    exist_arrangements = ShiftArrangement.query.filter_by(date=date(*reserve_date)).all()
    if exist_arrangements is not None and duty_id in [arr.did for arr in exist_arrangements]:
        return True
    else:
        return False

@bp.route('/book', methods = ['GET', 'POST'])
def book():
    cal = Calendar(0)
    today = date.today()
    cal_list = [[cal.monthdatescalendar(today.year+j, i+1) for i in range(12)] for j in range(2)]
    arrangements = ShiftArrangement.query.all()
    bookin_list = defaultdict(list)
    for arrangement in arrangements:
        bookin_list[str(arrangement.date)].append(arrangement.did)
    
    semester = Semester.query.order_by(Semester.id.desc()).first()
    delta =  semester.end_date - semester.start_date
    avaliable = []
    for i in range(delta.days + 1):
        day = semester.start_date + timedelta(days=i)
        if day.weekday() <= 4:
            avaliable.append(day)

    form = ReserveForm()
    if form.validate_on_submit():
        user_id = session['user_id']
        reserve_date = (int(form.year.data), int(form.month.data), int(form.day.data))
        duty_id = form.period.data
        form.period.data = ''

        exist_arrangements = ShiftArrangement.query.filter_by(date=date(*reserve_date)).all()

        if not is_period_duplicate(reserve_date, duty_id):
            db.session.add(ShiftArrangement(date=datetime(*reserve_date), uid=user_id, did=duty_id))
            db.session.commit()
        else:
            abort(500)

    return render_template('user/book.html', today=today, cal=cal_list, form=form, bookin_list=bookin_list, avaliable=avaliable)

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