from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    account = StringField("學號", validators = [DataRequired()])
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