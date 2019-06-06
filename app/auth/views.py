from flask import render_template, redirect, url_for, session, flash
from app.auth.forms import LoginForm, SingUp, ForgotPasswordForm, ChangePasswordForm
from app.auth import bp

@bp.route('/login', methods = ['GET', 'POST'])
def login():
    account = None
    password = None
    form = LoginForm()
    if form.validate_on_submit():
        account = form.account.data
        form.account.data = ''
        session['logged_in'] = True
        return redirect(url_for('user.dashboard'))

    
    return render_template('auth/login.html', form = form, account = account, password = password)

@bp.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SingUp()
    if form.validate_on_submit():
        account = form.account.data
        form.name.data = ''

        name = form.name.data
        form.name.data = ''

        email = form.email.data
        form.email.data = ''
    return render_template("auth/sign_up.html",  form = form)

@bp.route('/forgotpassword', methods = ['GET', 'POST'])
def forgotpassword():
    account = None
    email = None
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        account = form.account.data
        form.account.data = ''
        email = form.email.data
        form.email.data = ''
    return render_template('auth/forgot_pwd.html', form = form, account = account, email = email)

@bp.route('/logout')
def logout():
    session.pop('logged_in')
    return redirect(url_for('main.index'))

@bp.route('/changepassword', methods=['GET', 'POST'])
#@login_required  
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('密碼修改完成！')
            return redirect(url_for('logout'))
        else:
            flash('密碼不正確.')
    return render_template("auth/change_password.html", form=form)