from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    from app.main import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import bp as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.user import bp as user_blueprint
    app.register_blueprint(user_blueprint)

    from app.admin import bp as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from app.errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    return app
    
