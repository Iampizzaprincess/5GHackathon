from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    credits = db.Column(db.Float, default=0.00)

    def __init__(self, username, firstname, lastname, credits=0.00):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.credits = credits

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'credits': self.credits
        }
    
    def __repr__(self):
        return f'<User {self.id}: {self.username}>'

