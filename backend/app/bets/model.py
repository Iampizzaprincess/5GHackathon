from sqlalchemy import select
from app import db
from app.users import User

class BetUserAssociation(db.Model):
    __tablename__ = 'betuserassociation'

    user_id = db.Column(db.ForeignKey('bet.id'), primary_key=True)
    bet_id = db.Column(db.ForeignKey('user.id'), primary_key=True)

    def __init__(self, bet_id, user_id):
        self.bet_id = bet_id
        self.user_id = user_id

class Bet(db.Model):
    __tablename__ = 'bet'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))

    def __init__(self, description):
        self.description = description
    
    def get_users(self):
        stmt = select(User.id, User.username).join(BetUserAssociation.bet_id == id).join(BetUserAssociation.user_id == User.id)
        users = []
        for row in db.session.execute(stmt):
            users.append(row)
        return users
    
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description
        }

    def __repr__(self):
        return f'<Bet {self.id}: {self.description[:20]}>'

