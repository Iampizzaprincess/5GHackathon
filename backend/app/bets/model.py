from sqlalchemy import select
from app import db
from app.users import User

class BetUserAssociation(db.Model):
    __tablename__ = 'betuserassociation'
    NEUTRAL = 0
    AGAINST = 1
    FOR = 2

    user_id = db.Column(db.ForeignKey('bet.id'), primary_key=True)
    bet_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.Integer, default=NEUTRAL)
    like = db.Column(db.Boolean, default=False)
    wager = db.Column(db.Float, default=0.00)

    def __init__(self, bet_id, user_id, status=NEUTRAL, like=False, wager=0.00):
        self.bet_id = bet_id
        self.user_id = user_id
        self.status = status
        self.like = like
        self.wager = wager

class Bet(db.Model):
    __tablename__ = 'bet'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    approved = db.Column(db.Boolean, default=False)

    def __init__(self, description, approved=False):
        self.description = description
        self.approved = approved
    
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'approved': self.approved
        }

    def __repr__(self):
        return f'<Bet {self.id}: {self.description[:20]}>'

