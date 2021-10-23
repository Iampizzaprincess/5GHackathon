from sqlalchemy import select
from app import db
from app.users import User

class BetUserAssociation(db.Model):
    __tablename__ = 'betuserassociation'
    UNDECIDED = 0
    OPTION1 = 1
    OPTION2 = 2

    user_id = db.Column(db.ForeignKey('bet.id'), primary_key=True)
    bet_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    decision = db.Column(db.Integer, default=UNDECIDED)
    like = db.Column(db.Boolean, default=False)
    wager = db.Column(db.Float, default=0.00)

    def __init__(self, bet_id, user_id, decision=UNDECIDED, like=False, wager=0.00):
        self.bet_id = bet_id
        self.user_id = user_id
        self.decision = decision
        self.like = like
        self.wager = wager

class Bet(db.Model):
    __tablename__ = 'bet'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    approved = db.Column(db.Boolean, default=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)

    def __init__(self, description, option1, option2, approved=False):
        self.description = description
        self.approved = approved
        self.option1 = option1
        self.option2 = option2
    
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'approved': self.approved,
            'option1': self.option1,
            'option2': self.option2
        }

    def __repr__(self):
        return f'<Bet {self.id}: {self.description[:20]}>'

