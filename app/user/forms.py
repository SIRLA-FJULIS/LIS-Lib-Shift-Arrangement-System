from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class ContactForm(FlaskForm):
    topic = StringField("主旨", validators = [DataRequired()])
    email = EmailField("Emai",validators = [DataRequired()])
    content = TextAreaField("內容", validators = [DataRequired()])
    submit = SubmitField("送出")
