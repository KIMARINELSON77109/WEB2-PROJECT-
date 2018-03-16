import datetime
from . import db


class UserProfile(db.Model):
    user_ID = db.Column(db.String(255), primary_key=True)
    FirstName = db.Column(db.String(80), nullable=False)
    LastName = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    Email = db.Column(db.String(80), unique=True, nullable=False)
    Location = db.Column(db.String(255), nullable=False)
    Biography = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(80), nullable=False)
    created_on = db.Column(db.DateTime,nullable=False)
    
    __tablename__ = "UserProfile"
    
    def __init__(self,user_ID,FirstName,LastName,gender,Email,Location,Biography,photo,created_on):
        self.user_ID = user_ID
        self.FirstName = FirstName
        self.LastName = LastName
        self.gender = gender
        self.Email = Email
        self.Location = Location
        self.Biography = Biography
        self.photo = photo
        self.created_on = created_on

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
