from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#User model for the database 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String, nullable=False)

#Energy Usage 
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    appliance =  db.Column(db.String, unique=True, nullable=False)
    watts =  db.Column(db.Float, unique=True, nullable=False)
    hours =  db.Column(db.Float, unique=True, nullable=False)
    cost_per_kwh =  db.Column(db.Float, unique=True, nullable=False)
    time_period =  db.Column(db.String, unique=True, nullable=False)
        

def __repr__(self): 
        return f'<User {self.fullname}>'