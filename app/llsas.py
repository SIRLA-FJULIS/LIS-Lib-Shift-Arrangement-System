from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "llsas"
db_path = os.path.dirname(__file__)
db_path = os.path.join(db_path, 'llsas.db')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////{}".format(db_path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 減少記憶體使用

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup')
def signup():
    return render_template("sign_up.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
    
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500