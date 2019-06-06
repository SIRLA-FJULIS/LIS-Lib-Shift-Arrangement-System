from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from app.main import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import bp as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.user import bp as user_blueprint
    app.register_blueprint(user_blueprint)

    from app.admin import bp as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from app.errors import bp as errors_blueprint
    app.register_blueprint(errors_blueprint)

    return app
    