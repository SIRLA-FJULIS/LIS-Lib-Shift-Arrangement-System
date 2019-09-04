from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, StringField, TextAreaField
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