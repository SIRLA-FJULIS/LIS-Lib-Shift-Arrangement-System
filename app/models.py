from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return UserData.query.get(int(user_id))

class Permission:
    ADMIN = 1
    USER = 0
    UNKNOWN = -1

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key = True, index = True)
    name = db.Column(db.String(64), unique = True, index = True)
    default = db.Column(db.Boolean, default = False, index = True)
    permissions = db.Column(db.Integer)
    
    users = db.relationship('UserData', backref='role')

    def set_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions = perm

    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    @staticmethod
    def insert_roles():
        roles = {
            'Admin': Permission.ADMIN,
            'User': Permission.USER,
            'Unknown': Permission.UNKNOWN
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name = r).first()
            if role is None:
                role = Role(name = r)
                role.set_permission(roles[r])
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = -1

    def __repr__(self):
        return '<Role %r>' % self.name

class UserData(UserMixin, db.Model):
    __tablename__ = 'userData'
    id = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    name = db.Column(db.String(64), index = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String, unique = True, index = True)
    
    role_ref = db.Column(db.Integer, db.ForeignKey('role.id'), index = True)
    arrangements = db.relationship('ShiftArrangement', backref = 'user', lazy = 'dynamic')
    modification_ref = db.relationship('ModifyApplication', backref = 'user', lazy = 'dynamic')
    contact_ref = db.relationship('Contact', backref = 'user', lazy = 'dynamic')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
	
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, perm):
        return self.role_ref is not None and Role.query.filter_by(id=self.role_ref).first().has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def __init__(self, **kwargs):
        super(UserData, self).__init__(**kwargs)
        if self.role_ref is None:
            self.role_ref = Role.query.filter_by(default = True).first()

    def __repr__(self):
        return '<User %r:%r>' % (self.id, self.name)


class ShiftArrangement(db.Model):
    __tablename__ = 'shiftArrangement'
    id = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    date = db.Column(db.Date, index = True)
    checkIn = db.Column(db.DateTime, nullable = True)
    checkInState = db.Column(db.String(10), default = 'None')
    checkOut = db.Column(db.DateTime, nullable = True)
    checkOutState = db.Column(db.String(10), default = 'None')
    uid = db.Column(db.Integer, db.ForeignKey('userData.id'))
    did = db.Column(db.Integer, db.ForeignKey('duty.id'))
    modification = db.relationship('ModifyApplication', backref = 'arrangement', lazy = 'dynamic')
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'))
    def __repr__(self):
        return '<Arrangement %r : %r>' % (self.uid, self.date)


class ModifyApplication(db.Model):
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
        return '<Modification %r : %r - %r>' % (self.uid, self.date, self.period)


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    title = db.Column(db.String)
    dateTime = db.Column(db.DateTime)
    content = db.Column(db.Text)
    def __repr__(self):
        return '<News %r [%r]>' % (self.title, self.dateTime)

class Duty(db.Model):
    __tablename__ = 'duty'
    id = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    period = db.Column(db.String)
    content = db.Column(db.String)
    explanation = db.Column(db.Text)
    modification = db.relationship('ModifyApplication', backref = 'duty', lazy = 'dynamic')
    arrangement = db.relationship('ShiftArrangement', backref = 'duty', lazy = 'dynamic')
    def __repr__(self):
        return '<Duty %r - %r: %r>' % (self.id, self.period, self.content)

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    date = db.Column(db.Date)
    email = db.Column(db.String)
    content = db.Column(db.Text)
    uid = db.Column(db.Integer, db.ForeignKey('userData.id'))
    def __repr__(self):
        return '<Contact %r [%r]' % (self.date, self.email)

class Semester(db.Model):
    __tablename__ = 'semester'
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    name = db.Column(db.String)
    start_date = db.Column(db.Date, index=True)
    end_date = db.Column(db.Date, index=True)
    unavailableDates = db.relationship('UnavailableDate', backref='semester', lazy='dynamic')
    shiftArrangements = db.relationship('ShiftArrangement', backref='semester', lazy='dynamic')
    def __repr__(self):
        return '<Semester %r: %r - %r>' % (self.name, self.start_date, self.end_date)

class UnavailableDate(db.Model):
    __tablename__ = 'unavailableDate'
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    festival_name = db.Column(db.String)
    date = db.Column(db.Date, index=True)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'))
    def __repr__(self):
        return '<Unavailable Date: %r %r>' % (self.festival_name, self.date)