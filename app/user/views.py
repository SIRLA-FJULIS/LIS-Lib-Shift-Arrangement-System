from flask import render_template, redirect, url_for, request, session, abort
from app.user.forms import ContactForm, ReserveForm
from app.user import bp
from calendar import Calendar
from datetime import date, datetime, timedelta
from app.models import ShiftArrangement, Semester, UserData, Duty
from app import db
from collections import defaultdict
from flask_login import login_required, current_user

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

@bp.route('/user')
@login_required
def dashboard():
    arrangements = UserData.query.filter_by(id=current_user.id).first().arrangements.order_by(ShiftArrangement.date.asc()).all()
    # 日期(ShiftArrangement)、時間(Duty)、是否已輪值(ShiftArrangement)、工作項目(Duty)、工作說明(Duty)
    # arrangements_info = {
    #     'arr1': {
    #         'date': "",
    #         'time': "",
    #         'state': False,
    #         'work': "",
    #         'description': ""
    #     }, 
    #     'arr2': {
    #         'date': "",
    #         'time': "",
    #         'state': False,
    #         'work': "",
    #         'description': ""
    #     }
    # }   
    
    arrangements_info = []
    for arrangement in arrangements:
        arr_info = {}
        arr_info['date'] = arrangement.date
        arr_info['period'] = arrangement.duty.period
        
        # 判斷state: 尚未預約-NO_BOOKIN、已預約未簽到-RESERVED(簽到為False)、已簽到-DONE(簽到退皆為True)、尚未簽退-NOT_CHECKOUT(簽到為True、簽退為False)
        if arrangement.isCheckIn == True and arrangement.isCheckOut == True:
            arr_info['state'] = 'DONE'
        elif arrangement.isCheckIn == False:
            arr_info['state'] = 'RESERVED'
        elif arrangement.isCheckIn == True and arrangement.isCheckOut == False:
            arr_info['state'] = 'NOT_CHECKOUT'
        
        arr_info['content'] = arrangement.duty.content
        arr_info['explanation'] = arrangement.duty.explanation
    
        arrangements_info.append(arr_info)
    
    # 如果只有一筆預約就補一筆尚未預約，沒有任何預約的話就補兩筆
    if len(arrangements_info) == 1:
        arrangements_info.append({'state': 'NO_BOOKIN'})
    if len(arrangements_info) == 0:
        arrangements_info.append({'state': 'NO_BOOKIN'})
        arrangements_info.append({'state': 'NO_BOOKIN'})

    return render_template('user/dashboard.html', arrangements_info=arrangements_info)

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