from . import db

class UserDataTable(db.Model):
    __tablename__ = 'userData'
    userID = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    userName = db.Column(db.String(64), index = True)
    userPassword = db.Column(db.String)
    userEmail = db.Column(db.String, unique = True)
    userRole = db.Column(db.String, index = True)
    arrangements = db.relationship('ShiftArrangementTable', backref = 'user', lazy = 'dynamic')

    def __repr__(self):
        return '<User %r:%r>' % (self.userID, self.userName)

class ShiftArrangementTable(db.Model):
    __tablename__ = 'shiftArrangement'
    arrangementID = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    arrangementDate = db.Column(db.Date, index = True)
    arrangementPeriod = db.Column(db.String)
    arrangementCheckIn = db.Column(db.DateTime, nullable = True)
    arrangementCheckInState = db.Column(db.String(10), default = 'None')
    arrangementCheckOut = db.Column(db.DateTime, nullable = True)
    arrangementCheckOutState = db.Column(db.String(10), default = 'None')
    uID = db.Column(db.Integer, db.ForeignKey('userData.userID'))

    def __repr__(self):
        return '<Arrangement %r:%r>' % (self.uID, self.arrangementDate)