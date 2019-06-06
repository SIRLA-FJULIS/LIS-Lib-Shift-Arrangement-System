from flask import render_template
from app.admin.forms import CheckInOutForm
from app.admin import bp

@bp.route('/checkinout', methods = ['GET', 'POST'])
def check_in_out():
    form = CheckInOutForm()
    return render_template('admin/check_in_out.html', form = form)