from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Table_UserData.query.get(int(user_id))

class Table_UserData(UserMixin, db.Model):
    __tablename__ = 'userData'
    id = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    name = db.Column(db.String(64), index = True)
    password = db.Column(db.String(128))
    email = db.Column(db.String, unique = True, index = True)
    role = db.Column(db.String, index = True)
    id_for_arrangements = db.relationship('Table_ShiftArrangement', backref = 'user', lazy = 'dynamic')
    id_for_modification = db.relationship('Table_ModifyApplication', backref = 'user', lazy = 'dynamic')
    id_for_contact = db.relationship('Table_Contact', backref = 'user', lazy = 'dynamic')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
	
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r:%r>' % (self.userID, self.userName)


class Table_ShiftArrangement(db.Model):
    __tablename__ = 'shiftArrangement'
    id = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    date = db.Column(db.Date, index = True)
    checkIn = db.Column(db.DateTime, nullable = True)
    checkInState = db.Column(db.String(10), default = 'None')
    checkOut = db.Column(db.DateTime, nullable = True)
    checkOutState = db.Column(db.String(10), default = 'None')
    uid = db.Column(db.Integer, db.ForeignKey('userData.id'))
    did = db.Column(db.Integer, db.ForeignKey('duty.id'))
    modification = db.relationship('Table_ModifyApplication', backref = 'arrangement', lazy = 'dynamic')
    def __repr__(self):
        return '<Arrangement %r : %r>' % (self.uID, self.arrangementDate)


class Table_ModifyApplication(db.Model):
    """
    Apply to modify the shift arrangement.
    """
    __tablename__ = 'modifyApplication'
    id = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    date = db.Column(db.Date)
    reason = db.Column(db.String)
    uid = db.Column(db.Integer, db.ForeignKey('userData.id'))
    aid = db.Column(db.Integer, db.ForeignKey('shiftArrangement.id'))
    did = db.Column(db.Integer, db.ForeignKey('duty.id'))
    def __repr__(self):
        return '<Modification %r : %r - %r>' % (self.uID, self.modifyDate, self.modifyPeriod)


class Table_News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    title = db.Column(db.String)
    dateTime = db.Column(db.DateTime)
    content = db.Column(db.Text)
    def __repr__(self):
        return '<News %r [%r]>' % (self.newsTitle, self.newsDateTime)

class Table_Duty(db.Model):
    __tablename__ = 'duty'
    id = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    period = db.Column(db.String)
    content = db.Column(db.String)
    explanation = db.Column(db.Text)
    modification = db.relationship('Table_ModifyApplication', backref = 'duty', lazy = 'dynamic')
    arrangement = db.relationship('Table_ShiftArrangement', backref = 'duty', lazy = 'dynamic')
    def __repr__(self):
        return '<Duty %r - %r: %r>' % (self.dutyID, self.dutyPeriod, self.dutyContent)

class Table_Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    date = db.Column(db.Date)
    email = db.Column(db.String)
    content = db.Column(db.Text)
    uid = db.Column(db.Integer, db.ForeignKey('userData.id'))
    def __repr__(self):
        return '<Contact %r [%r]' % (self.contactDate, self.contactEmail)