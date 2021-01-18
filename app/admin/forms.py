# -*- coding: UTF-8 -*-
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import DateField, SubmitField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email
from datetime import datetime

class CheckInOutForm(FlaskForm):
    student_id = StringField('輸入學號', validators=[DataRequired()])
    submit_in_out = SubmitField("簽到/退")

class NewsForm(FlaskForm):
    title = StringField("標題")
    date_time = DateField('發布時間', default=datetime.now)
    content = TextAreaField("內容")
    submit = SubmitField("確定")

class DutyForm(FlaskForm):
	content = StringField("工作內容")
	explanation = TextAreaField("工作內容說明")
	submit = SubmitField("確定")

class ManageDateForm(FlaskForm):
    festival_name = StringField("節假日名稱", validators=[DataRequired()])
    date = DateField('日期', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("確定")

class AddSemesterFrom(FlaskForm):
    name = StringField("學期名稱")
    start_date = DateField('輪值開放日期', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('輪值結束日期', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("確定")
    
class AddUserForm(FlaskForm):
    name = StringField("姓名", validators=[DataRequired()])
    id = StringField("學號", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("新增")

class BatchAddUserForm(FlaskForm):
    file = FileField('添加檔案', validators=[FileRequired(), FileAllowed(['xls', 'xlsx', 'xlsb'], '請上傳excel檔！')])
    submit = SubmitField("上傳")
    
class DelUserForm(FlaskForm):
    del_id = StringField("學號", validators=[DataRequired()])
    submit = SubmitField("刪除")

class DelSemesterForm(FlaskForm):
    del_semester = StringField("學期名稱", validators=[DataRequired()])
    submit = SubmitField("刪除")

class DelManage_dateForm(FlaskForm):
    del_manage_date = StringField("假期名稱", validators=[DataRequired()])
    submit = SubmitField("刪除")