from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField

class BookForm(FlaskForm):
    time1 =BooleanField('8:30-10:00')
    time2 =BooleanField('10:00-12:00')
    time3 =BooleanField('12:00-13:00')
    time4 =BooleanField('13:30-15:30')
    time5 =BooleanField('15:30-17:30')
    submit = SubmitField("送出")

class ContactForm(FlaskForm):
    topic = StringField("主旨", validators = [DataRequired()])
    email = EmailField("Emai",validators = [DataRequired()])
    content = StringField("內容", validators = [DataRequired()])
    submit = SubmitField("送出")
