from flask import Flask, render_template, session, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = "llsas"
db_path = os.path.dirname(__file__)
db_path = os.path.join(db_path, 'llsas.db')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////{}".format(db_path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 減少記憶體使用

db = SQLAlchemy(app)
class LoginForm(FlaskForm):
    account = StringField("學號", validators = [DataRequired()])
    password = PasswordField("密碼")
    submit = SubmitField("送出")

class SingUp(FlaskForm):
    account = StringField("學號", validators = [DataRequired()])
    name = StringField("姓名", validators = [DataRequired()])
    email = EmailField("電子信箱", validators = [DataRequired(), Email()])
    password = PasswordField("密碼")
    submit = SubmitField("送出")

class ForgotPasswordForm(FlaskForm):
    account = StringField("學號", validators = [DataRequired()])
    email = EmailField("電子信箱", validators = [DataRequired(), Email()])
    submit = SubmitField("Submit")

class ChangePasswordForm(FlaskForm):
    password_old = PasswordField("舊密碼", validators = [DataRequired()])
    password_new = PasswordField("新密碼", validators = [DataRequired(),EqualTo("password_new_confirm", message="PASSWORD NEED MATCH")])
    password_new_confirm = PasswordField("確認新密碼", validators=[DataRequired()])
    submit = SubmitField("更改密碼")

class Book(FlaskForm):
    time1 =BooleanField('8:30-10:00')
    time2 =BooleanField('10:00-12:00')
    time3 =BooleanField('12:00-13:00')
    time4 =BooleanField('13:30-15:30')
    time5 =BooleanField('15:30-17:30')
    submit = SubmitField("送出")

class CheckinStatus(FlaskForm):
    time= DateField('刷卡時間', format='%Y:%m:%d')
    submit_in = SubmitField("簽到")
    submit_out = SubmitField("簽退")

@app.route('/1')
def index():
   return render_template("index.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    account = None
    password = None
    form = LoginForm()
    if form.validate_on_submit():
        account = form.account.data
        form.account.data = ''
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    return render_template('login.html', form = form, account = account, password = password)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SingUp()
    if form.validate_on_submit():
        account = form.account.data
        form.name.data = ''

        name = form.name.data
        form.name.data = ''

        email = form.email.data
        form.email.data = ''
    return render_template("sign_up.html",  form = form)

@app.route('/forgotpassword', methods = ['GET', 'POST'])
def forgotpassword():
    account = None
    email = None
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        account = form.account.data
        form.account.data = ''
        email = form.email.data
        form.email.data = ''
    return render_template('forgot_pwd.html', form = form, account = account, email = email)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('logged_in')
    return redirect(url_for('index'))

@app.route('/book', methods = ['GET', 'POST'])
def book():
    form = Book()
    return render_template('book.html', form = form)

@app.route('/chekcin_status', methods = ['GET', 'POST'])
def checkinstatus():
    form = CheckinStatus()
    return render_template('checkin_status.html', form = form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
    
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

@app.route('/changepassword', methods=['GET', 'POST'])
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
    return render_template("change_password.html", form=form)