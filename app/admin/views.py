from flask import render_template, redirect, url_for, request, make_response
from app.admin.forms import CheckInOutForm, NewsForm, DutyForm, ManageDateForm, AddSemesterFrom, AddUserForm, BatchAddUserForm
from app.admin import bp
from app import db
from app.models import Duty, Semester, UnavailableDate, News, UserData, ShiftArrangement
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from calendar import Calendar
from datetime import date, datetime, timedelta
from ..decorators import admin_required
from flask_login import current_user, login_required
from collections import defaultdict
from io import BytesIO
import xlsxwriter
import json
import datetime

def create_workbook():
    output = BytesIO()
    # 創建Excel文件,不保存,直接輸出
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    # 設置檔名為student_data
    worksheet = workbook.add_worksheet('student_data')
    # 標題
    title = ["學號","姓名","簽到時間1","簽到時間2","輪值次數"]
    worksheet.write_row('A1', title)

    student = UserData.query.filter_by(role_ref=2).all()
    count = 0
    for i in student:
        output_data = [i.id, i.name,'0','0','0']
        status = ShiftArrangement.query.filter_by(uid=i.id).all()
        
        for j in status:
            print(j.checkInTime)
            if j.isCheckIn == True and j.isCheckOut == True and output_data[-1] == '0':
                output_data[2] = str(j.checkInTime)
                output_data[-1] = '1'
            elif j.isCheckIn == True and j.isCheckOut == True and output_data[-1] == '1':
                output_data[3] = str(j.checkInTime)
                output_data[-1] = '2'

        worksheet.write_row('A' + str(count + 2), output_data)
        count += 1
    '''
    dictList = [{"a":"a1","b":"b1","c":"c1"},{"a":"a2","b":"b2","c":"c2"},{"a":"a3","b":"b3","c":"c3"}]
    for i in range(len(dictList)):
        row = [dictList[i]["a"],dictList[i]["b"],dictList[i]["c"]]
        worksheet.write_row('A' + str(i + 2), row)
    '''


    workbook.close()
    response = make_response(output.getvalue())
    output.close()
    return response

@bp.route('/checkinout', methods = ['GET', 'POST'])
@login_required
@admin_required
def check_in_out():
    form = CheckInOutForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        today = datetime.date.today()
        time_now = datetime.datetime.now()
        
        arrangements = ShiftArrangement.query.filter_by(uid=student_id, date=today).all()
        
        for i in arrangements:
            work_time = Duty.query.filter_by(id=i.did).first()
            work_time_start = work_time.period.split('~')[0].split(":")
            work_time_end = work_time.period.split('~')[1].split(":")

            #確定是要哪個時段
            if int(work_time_end[0]) < time_now.hour and int(work_time_end[1]) + 15 < time_now.minute:
                continue
            print(work_time)

            if time_now.hour - int(work_time_start[0]) == 0 and time_now.minute -  int(work_time_start[1]) <= 15 and i.isCheckIn == False:
                i.checkInTime = time_now
                i.isCheckIn = True
                print(i)
                db.session.commit()
                break
                
            elif time_now.hour - int(work_time_end[0]) == 0 and time_now.minute -  int(work_time_end[1]) <= 15 and i.isCheckIn == True:
                i.checkOutTimes = time_now
                i.isCheckOut = True
                print(i)
                db.session.commit()
                break
                

        print(arrangements)
    return render_template('admin/check_in_out.html', form = form)

@bp.route('/admin_dashboard', methods = ['GET', 'POST'])
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

@bp.route('/news_management/<int:page>/', methods = ['GET', 'POST'])
@login_required
@admin_required
def news_management(page=1):
    news = News.query.order_by(News.dateTime.desc()).paginate(page, 10, False)
    #print(news)
    return render_template('admin/news_management.html', news = news)

@bp.route('/edit_news/<id>', methods = ['GET', 'POST'])
@login_required
@admin_required
def edit_news(id):
    news = News.query.filter_by(id=id).first()
    form = NewsForm()
    if form.validate_on_submit():
        news.title = form.title.data
        news.dateTime = form.date_time.data
        news.content = form.content.data
        db.session.commit()
        return redirect(url_for('admin.news_management', page=1))
    form.title.data = news.title
    form.date_time.data = news.dateTime
    form.content.data = news.content
    return render_template('admin/edit_news.html', form = form, news = news)

@bp.route('/delete_news/<id>', methods = ['GET', 'POST'])
@login_required
@admin_required
def delete_news(id):
    news_to_delete = News.query.get_or_404(id)
    try:
        db.session.delete(news_to_delete)
        db.session.commit()
        return redirect(url_for('admin.news_management', page=1))
    except:
        return render_template('admin/news_management.html')

@bp.route('/add_news', methods = ['GET', 'POST'])
@login_required
@admin_required
def add_news():
    form = NewsForm()
    #form.date_time.data = datetime.date.today()
    if form.validate_on_submit():
        db.session.add(News(title=form.title.data, dateTime=form.date_time.data, content=form.content.data))
        db.session.commit()
        return redirect(url_for('admin.news_management', page=1))
    return render_template('admin/add_news.html', form = form)

@bp.route('/duty_management', methods = ['GET', 'POST'])
@login_required
@admin_required
def duty_management():
    duties = Duty.query.order_by(Duty.id.asc()).all()
    print(duties)
    return render_template('admin/duty_management.html', duties=duties)

@bp.route('/edit_duty/<id>', methods = ['GET', 'POST'])
@login_required
@admin_required
def edit_duty(id):
    duty = Duty.query.filter_by(id=id).first()
    form = DutyForm()
    if form.validate_on_submit():
        duty.content = form.content.data
        duty.explanation = form.explanation.data
        db.session.commit()
        return redirect(url_for('admin.duty_management'))
    form.content.data = duty.content
    form.explanation.data = duty.explanation
    return render_template('admin/edit_duty.html', form=form, period=duty.period)

@bp.route('/manage_date', methods = ['GET', 'POST'])
@login_required
@admin_required
def manage_date():
    form = ManageDateForm()
    if form.validate_on_submit():
        current_semester_id = Semester.query.order_by(Semester.id.desc()).first().id
        db.session.add(UnavailableDate(festival_name=form.festival_name.data, date=form.date.data, semester_id=current_semester_id))
        db.session.commit()
        form.festival_name.data = ''
        form.date.data = ''
        return redirect(url_for('admin.manage_date'))
    return render_template('admin/manage_date.html', form = form)

@bp.route('/add_semester', methods = ['GET', 'POST'])
@login_required
@admin_required
def add_semester():
    form = AddSemesterFrom()
    if form.validate_on_submit():
        db.session.add(Semester(name=form.name.data, start_date=form.start_date.data, end_date=form.end_date.data))
        db.session.commit()
        form.name.data = ''
        form.start_date.data = ''
        form.end_date.data = ''
        return redirect(url_for('admin.add_semester'))
    return render_template('admin/add_semester.html', form = form)

@bp.route('/add_user', methods = ['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        db.session.add(UserData(id = form.id.data, name = form.name.data, email = form.email.data, password = form.id.data, role_ref = 2))
        db.session.commit()
        form.id.data = ''
        form.name.data = ''
        form.email.data = ''
        return redirect(url_for('admin.add_user'))
        
    return render_template('admin/add_user.html', form = form)

@bp.route('/batch_add_user', methods = ['GET', 'POST'])
@login_required
@admin_required
def batch_add_user():
    form = BatchAddUserForm()
    
    if form.validate_on_submit():
        df = pd.read_excel(form.file.data)# df:dataframe
        print(df)
        for i, data in df.iterrows():
            name = data['姓名']
            id = data['學號']
            email = data['email']
            db.session.add(UserData(id = id, name = str(name), email = email, password = str(id), role_ref = 2))
            db.session.commit()
    return render_template('admin/batch_add_user.html', form = form)

@bp.route('/news', methods = ['GET', 'POST'])
@login_required
@admin_required
def news(page=1):
    news = News.query.order_by(News.dateTime.desc()).paginate(page, 10, False)
    #print(news)
    return render_template('admin/news.html', news = news)

@bp.route('/news/<id>', methods=['POST', 'GET'])
@login_required
@admin_required
def news_detail(id):
    news_content = News.query.filter_by(id=id).first()
    return render_template('admin/news_content.html', news_content = news_content)

@bp.route('/book_management', methods = ['GET', 'POST'])
@login_required
@admin_required
def book_management():
    cal = Calendar(0)
    today = date.today()
    cal_list = [[cal.monthdatescalendar(today.year+j, i+1) for i in range(12)] for j in range(2)]
    arrangements = ShiftArrangement.query.all()
    
    bookin_list = defaultdict(list)
    for arrangement in arrangements:
        bookin_list[str(arrangement.date)].append(arrangement.did)
    
    duties = Duty.query.all()

    semester = Semester.query.order_by(Semester.id.desc()).first()
    unavailable_dates = {unavailable_date.date: unavailable_date.festival_name for unavailable_date in semester.unavailableDates.all()}
    delta = semester.end_date - semester.start_date
    available_date = []
    for i in range(delta.days + 1):
        day = semester.start_date + timedelta(days=i)
        if day.weekday() <= 4 and day not in unavailable_dates:
            available_date.append(day)
            
    return render_template('admin/book_management.html', today=today, cal=cal_list, bookin_list=bookin_list, available_date=available_date, festivals=unavailable_dates, duties=duties)

@bp.route('/bookin_detail', methods = ['GET'])
@login_required
@admin_required
def get_bookin_detail():
    year, month, day = request.args.get('date').split('-')
    query_date = f'{year.zfill(4)}-{month.zfill(2)}-{day.zfill(2)}'
    arrangements = ShiftArrangement.query.filter_by(date=query_date).all()

    bookin_detail = []
    for arrangement in arrangements:
        bookin_detail.append({
            "duty_id": arrangement.duty.id,
            "student_id": arrangement.user.id,
            "student_name": arrangement.user.name,
            "arrangement_id": arrangement.id
        })
    
    return json.dumps(bookin_detail, ensure_ascii=False)

@bp.route('/delete_arrangement', methods = ['GET'])
@login_required
@admin_required
def delete_arrangement():
    arrangement_id = request.args.get('id')
    ShiftArrangement.query.filter_by(id=arrangement_id).delete()
    db.session.commit()

    return redirect(url_for('admin.book_management'))

@bp.route('/download', methods=['GET'])
def download():
    response = create_workbook()
    response.headers['Content-Type'] = "utf-8"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Content-Disposition"] = "attachment; filename=student_data.xlsx"
    return response