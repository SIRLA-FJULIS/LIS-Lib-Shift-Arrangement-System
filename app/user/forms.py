# -*- coding: UTF-8 -*-
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, SelectField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class ContactForm(FlaskForm):
    topic = StringField("主旨", validators = [DataRequired()])
    email = EmailField("Emai",validators = [DataRequired()])
    content = TextAreaField("內容", validators = [DataRequired()])
    submit = SubmitField("送出")

class ReserveForm(FlaskForm):
    year = HiddenField("year")
    month = HiddenField("month")
    day = HiddenField("day")
    period = SelectField("時段", choices=[(1, '時段一'), (2, '時段二'), (3, '時段三'), (4, '時段四'), (5, '時段五')], validators=[DataRequired()], coerce=int)