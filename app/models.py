from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

import datetime

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(USER_ID=user_id).first()

class  User(db.Model, UserMixin):
    __tablename__ = 'USERS'
    USER_ID  = db.Column(db.Integer, autoincrement=True, primary_key=True)
    USER_NAME = db.Column(db.String(86), nullable=False)
    USER_EMAIL = db.Column(db.String(84), nullable=False, unique=True)
    USER_HASH_PASSWORD = db.Column(db.String(128), nullable=False)
    USER_ACCESS_LEVEL = db.Column(db.Integer(), nullable=False)
    USER_STATUS = db.Column(db.Integer(), nullable=False)
    USER_LAST_ACCESS = db.Column(db.DateTime, nullable=False)
    USER_DATE_REGISTER = db.Column(db.DateTime, nullable=False)
    


    def  __init__(self, name, email, password):
        self.USER_NAME = name
        self.USER_EMAIL = email
        self.USER_HASH_PASSWORD = generate_password_hash(password)
        self.USER_ACCESS_LEVEL = 1
        self.USER_STATUS = 1
        self.USER_LAST_ACCESS = datetime.datetime.now()
        self.USER_DATE_REGISTER = datetime.datetime.now()
        

    def get_id(self):
        return (self.USER_ID)
        
    def verify_password(self, password):
        return check_password_hash(self.USER_HASH_PASSWORD, password)

db.create_all()