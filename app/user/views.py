from flask import render_template, redirect, url_for, request, session, abort
from app.user.forms import ContactForm, ReserveForm
from app.user import bp
from calendar import Calendar
from datetime import date, datetime, timedelta
from app.models import ShiftArrangement, Semester
from app import db
from collections import defaultdict
from flask_login import login_required, current_user

@bp.route('/user')
@login_required
def dashboard():
    return render_template('user/dashboard.html')

# check if period was booked
def is_period_duplicate(reserve_date, duty_id):
    exist_arrangements = ShiftArrangement.query.filter_by(date=date(*reserve_date)).all()
    if exist_arrangements is not None and duty_id in [arr.did for arr in exist_arrangements]:
        return True
    else:
        return False

# check if the user was already book tow arrangement in the semester
def is_arrangement_full(semester_id):
    arrangements_in_semester = current_user.arrangements.filter_by(semester_id=semester_id).all()
    return len(arrangements_in_semester) >= 2

@bp.route('/book', methods = ['GET', 'POST'])
@login_required
def book():
    cal = Calendar(0)
    today = date.today()
    cal_list = [[cal.monthdatescalendar(today.year+j, i+1) for i in range(12)] for j in range(2)]
    arrangements = ShiftArrangement.query.all()
    bookin_list = defaultdict(list)
    for arrangement in arrangements:
        bookin_list[str(arrangement.date)].append(arrangement.did)
    
    semester = Semester.query.order_by(Semester.id.desc()).first()
    unavailable_dates = {unavailable_date.date: unavailable_date.festival_name for unavailable_date in semester.unavailableDates.all()}
    delta =  semester.end_date - semester.start_date
    avaliable_date = []
    for i in range(delta.days + 1):
        day = semester.start_date + timedelta(days=i)
        if day.weekday() <= 4 and day not in unavailable_dates:
            avaliable_date.append(day)
    
    form = ReserveForm()
    if form.validate_on_submit():
        user_id = current_user.id
        reserve_date = (int(form.year.data), int(form.month.data), int(form.day.data))
        duty_id = form.period.data
        form.period.data = ''
        exist_arrangements = ShiftArrangement.query.filter_by(date=date(*reserve_date)).all()
        if not is_arrangement_full(semester.id) \
           and not is_period_duplicate(reserve_date, duty_id) \
           and date(*reserve_date) in avaliable_date:
            db.session.add(ShiftArrangement(date=datetime(*reserve_date), uid=user_id, did=duty_id, semester_id=semester.id))
            db.session.commit()
        elif is_arrangement_full(semester.id):
            return abort(400, {'message': '已預約兩次，不需要再預約了喔!'})
        elif date(*reserve_date) in avaliable_date:
            return abort(400, {'message': 'Reserve date not in available date'})
        elif is_period_duplicate(reserve_date, duty_id):
            return abort(400, {'message': 'Reservation was booked'})
        else:
            abort(500)
            

    return render_template('user/book.html', today=today, cal=cal_list, form=form, bookin_list=bookin_list, avaliable_date=avaliable_date, festivals=unavailable_dates)

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