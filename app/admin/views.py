from flask import render_template, redirect, url_for
from app.admin.forms import CheckInOutForm, NewsForm, DutyForm, ManageDateForm, AddSemesterFrom
from app.admin import bp
from app import db
from app.models import Duty, Semester, UnavailableDate, News
from flask_sqlalchemy import SQLAlchemy

import datetime

@bp.route('/checkinout', methods = ['GET', 'POST'])
def check_in_out():
    form = CheckInOutForm()
    return render_template('admin/check_in_out.html', form = form)

@bp.route('/admin_dashboard', methods = ['GET', 'POST'])
def dashboard():
    return render_template('admin/dashboard.html')

@bp.route('/news_management/<int:page>/', methods = ['GET', 'POST'])
def news_management(page=1):
    news = News.query.order_by(News.postTime.desc()).paginate(page, 10, False)
    #print(news)
    return render_template('admin/news_management.html', news = news)

@bp.route('/edit_news/<id>', methods = ['GET', 'POST'])
def edit_news(id):
    news = News.query.filter_by(id=id).first()
    form = NewsForm()
    if form.validate_on_submit():
        news.title = form.title.data
        news.postTime = form.post_time.data
        news.content = form.content.data
        db.session.commit()
        return redirect(url_for('admin.news_management', page=1))
    form.title.data = news.title
    form.post_time.data = news.postTime
    form.content.data = news.content
    return render_template('admin/edit_news.html', form = form, news = news)

@bp.route('/delete_news/<id>', methods = ['GET', 'POST'])
def delete_news(id):
    news_to_delete = News.query.get_or_404(id)
    try:
        db.session.delete(news_to_delete)
        db.session.commit()
        return redirect(url_for('admin.news_management', page=1))
    except:
        return render_template('admin/news_management.html')

@bp.route('/add_news', methods = ['GET', 'POST'])
def add_news():
    form = NewsForm()
    #form.post_time.data = datetime.date.today()
    if form.validate_on_submit():
        db.session.add(News(title=form.title.data, postTime=form.post_time.data, content=form.content.data))
        db.session.commit()
        return redirect(url_for('admin.news_management', page=1))
    return render_template('admin/add_news.html', form = form)

@bp.route('/duty_management', methods = ['GET', 'POST'])
def duty_management():
    duties = Duty.query.order_by(Duty.id.asc()).all()
    print(duties)
    return render_template('admin/duty_management.html', duties=duties)

@bp.route('/edit_duty/<id>', methods = ['GET', 'POST'])
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