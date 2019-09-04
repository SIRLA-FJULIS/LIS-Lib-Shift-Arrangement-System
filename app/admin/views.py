from flask import render_template
from app.admin.forms import CheckInOutForm, NewsForm
from app.admin import bp

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