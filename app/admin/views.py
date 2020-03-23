from flask import render_template, redirect, url_for
from app.admin.forms import CheckInOutForm, NewsForm, DutyForm, ManageDateForm
from app.admin import bp
from app import db
from app.models import Duty, Semester, UnavailableDate
from flask_sqlalchemy import SQLAlchemy

@bp.route('/checkinout', methods = ['GET', 'POST'])
def check_in_out():
    form = CheckInOutForm()
    return render_template('admin/check_in_out.html', form = form)

@bp.route('/admin_dashboard', methods = ['GET', 'POST'])
def dashboard():
    return render_template('admin/dashboard.html')

@bp.route('/add_news', methods = ['GET', 'POST'])
def add_news():
    form = NewsForm()
    title = form.title.data
    form.title.data = ''

    post_time = form.post_time.data
    form.post_time.data = ''

    content = form.content.data
    form.content.data = ''
    return render_template('admin/add_news.html', form = form, title = title, post_time = post_time, content = content)

@bp.route('/admin_news', methods = ['GET', 'POST'])
def news():
    form = NewsForm()
    return render_template('admin/news.html', form = form)

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