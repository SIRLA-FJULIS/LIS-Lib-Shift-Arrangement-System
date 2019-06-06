from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField

class CheckInOutForm(FlaskForm):
    time= DateField('刷卡時間', format='%Y:%m:%d')
    submit_in = SubmitField("簽到")
    submit_out = SubmitField("簽退")