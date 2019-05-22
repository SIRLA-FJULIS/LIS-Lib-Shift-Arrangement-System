from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

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

class ForgotPasswordForm(FlaskForm):
    account = StringField("Account", validators = [DataRequired()])
    email = EmailField("Email", validators = [DataRequired(), Email()])
    submit = SubmitField("Submit")
    
@app.route('/')
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
    return render_template('login.html', form = form, account = account, password = password)

@app.route('/signup')
def signup():
    return render_template("sign_up.html")

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
    
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500