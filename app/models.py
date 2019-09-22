from . import db

class Table_UserData(db.Model):
    __tablename__ = 'userData'
    userID = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    userName = db.Column(db.String(64), index = True)
    userPassword = db.Column(db.String)
    userEmail = db.Column(db.String, unique = True)
    userRole = db.Column(db.String, index = True)
    ID_for_arrangements = db.relationship('Table_ShiftArrangement', backref = 'user', lazy = 'dynamic')
    ID_for_modification = db.relationship('Table_ModifyApplication', backref = 'user', lazy = 'dynamic')
    ID_for_contact = db.relationship('Table_Contact', backref = 'user', lazy = 'dynamic')
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
    uid = db.Column(db.Integer, db.ForeignKey('Table_UserData.userID'))
    did = db.Column(db.Integer, db.ForeignKey('Table_Duty.dutyID'))
    modification = db.relationship('Table_ModifyApplication', backref = 'arrangement', lazy = 'dynamic')
    def __repr__(self):
        return '<Arrangement %r : %r>' % (self.uID, self.arrangementDate)


class Table_ModifyApplication(db.Model):
    """
    Apply to modify the shift arrangement.
    """
    __tablename__ = 'modifyApplication'
    modifyDate = db.Column(db.Date)
    modifyReason = db.Column(db.String)
    uID = db.Column(db.Integer, db.ForeignKey('Table_UserData.userID'))
    aID = db.Column(db.Integer, db.ForeignKey('Table_ShiftArrangement.arrangementID'))
    dID = db.Column(db.Integer, db.ForeignKey('Table_Duty.dutyID'))
    def __repr__(self):
        return '<Modification %r : %r - %r>' % (self.uID, self.modifyDate, self.modifyPeriod)


class Table_News(db.Model):
    __tablename__ = 'news'
    newsTitle = db.Column(db.String)
    newsDateTime = db.Column(db.DateTime)
    newsContent = db.Column(db.Text)
    def __repr__(self):
        return '<News %r [%r]>' % (self.newsTitle, self.newsDateTime)

class Table_Duty(db.Model):
    __tablename__ = 'duty'
    dutyID = db.Column(db.Integer, primary_key = True, unique = True, index = True)
    dutyPeriod = db.Column(db.String)
    dutyContent = db.Column(db.String)
    dutyExplanation = db.Column(db.Text)
    modification = db.relationship('Table_ModifyApplication', backref = 'duty', lazy = 'dynamic')
    arrangement = db.relationship('Table_ShiftArrangement', backref = 'duty', lazy = 'dynamic')
    def __repr__(self):
        return '<Duty %r - %r: %r>' % (self.dutyID, self.dutyPeriod, self.dutyContent)

class Table_Contact(db.Model):
    __tablename__ = 'contact'
    contactDate = db.Column(db.Date)
    contactEmail = db.Column(db.String)
    contactContent = db.Column(db.Text)
    uID = db.Column(db.Integer, db.ForeignKey('Table_UserData.userID'))
    def __repr__(self):
        return '<Contact %r [%r]' % (self.contactDate, self.contactEmail)