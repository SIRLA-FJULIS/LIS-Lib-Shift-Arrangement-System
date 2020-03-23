import os
from app import create_app, db
from flask_migrate import Migrate, upgrade
from app.models import *

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, UserData=UserData, Duty=Duty, ShiftArrangement=ShiftArrangement, Semester=Semester, UnavailableDate=UnavailableDate, Role=Role)

if __name__ == '__main__':
	app.run()
