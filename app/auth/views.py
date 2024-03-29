# -*- coding: UTF-8 -*-
from flask import render_template, redirect, url_for, session, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from app.auth.forms import LoginForm, ForgotPasswordForm, ChangePasswordForm
from app.auth import bp
from app import db
from app.models import UserData

@bp.route('/login', methods = ['GET', 'POST'])
def login():
    account = None
    password = None
    form = LoginForm()

    if form.validate_on_submit():
        account = form.account.data
        password = form.password.data
        user = UserData.query.filter_by(id = account).first()
        form.account.data = ''
        
        if user is not None and user.verify_password(password):
            login_user(user)
            next = request.args.get('next')
            
            if user.role_ref == 1:
                session['role'] = 'Admin'
                next = url_for('admin.dashboard')
            else:
                session['role'] = 'User'
                next = url_for('user.dashboard')
                
            return redirect(next)
        else:
            flash('Invalid account or password')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form = form)

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
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/changepassword', methods=['GET', 'POST'])
@login_required  
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password_old.data):
            
            current_user.password = form.password_new.data
            db.session.commit()
            #db.session.add(current_user)
            flash('密碼修改完成！')
            
            form.password_old.data = ""
            form.password_new.data = ""
            form.password_new_confirm.data = ""

            logout_user()
            return redirect(url_for('main.index'))
        else:
            flash('密碼不正確.')
    return render_template("auth/change_password.html", form=form)
