from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime

class CheckInOutForm(FlaskForm):
    time = DateField('刷卡時間', format='%Y-%m-%d')
    submit_in = SubmitField("簽到")
    submit_out = SubmitField("簽退")

class NewsForm(FlaskForm):
    title = StringField("標題")
    post_time = DateField('發布時間', format='%Y-%m-%d', default=datetime.today())
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