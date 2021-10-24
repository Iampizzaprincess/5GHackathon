from sqlalchemy import select
from app import db
from app.users import User

class BetUserAssociation(db.Model):
    __tablename__ = 'betuserassociation'
    UNCHOSEN = 0
    OPTION1 = 1
    OPTION2 = 2

    user_id = db.Column(db.ForeignKey('bet.id'), primary_key=True)
    bet_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    option = db.Column(db.Integer, default=UNCHOSEN)
    like = db.Column(db.Boolean, default=False)
    wager = db.Column(db.Float, default=0.00)

    def __init__(self, bet_id, user_id, option=UNCHOSEN, like=False, wager=0.00):
        self.bet_id = bet_id
        self.user_id = user_id
        self.option = option
        self.like = like
        self.wager = wager
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'bet_id': self.bet_id,
            'option': self.option,
            'like': self.like,
            'wager': self.wager
        }

class Bet(db.Model):
    __tablename__ = 'bet'
    ONGOING = 0
    OPTION1_WON = 1
    OPTION2_WON = 2

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    approved = db.Column(db.Boolean, default=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    min_wager = db.Column(db.Float, default=0.00)
    winner = db.Column(db.Integer, default=-1)

    def __init__(self, description, option1, option2, min_wager=0.00, approved=False):
        self.description = description
        self.approved = approved
        self.option1 = option1
        self.option2 = option2
        self.min_wager = min_wager
    
    def to_dict(self):
        stmt = select(
            BetUserAssociation.option, BetUserAssociation.like, BetUserAssociation.wager
        ).\
        join(User, BetUserAssociation.user_id == User.id).\
        filter(BetUserAssociation.bet_id == self.id)

        nUnchosen = 0
        nOption1 = 0
        nOption2 = 0
        pot = 0.0
        nLikes = 0
        for row in db.session.execute(stmt):
            if row.option == BetUserAssociation.UNCHOSEN: nUnchosen += 1
            if row.option == BetUserAssociation.OPTION1: nOption1 += 1
            if row.option == BetUserAssociation.OPTION2: nOption2 += 1
            if row.like : nLikes += 1
            if row.option != BetUserAssociation.UNCHOSEN: pot += row.wager

        return {
            'id': self.id,
            'description': self.description,
            'approved': self.approved,
            'option1': self.option1,
            'option2': self.option2,
            'min_wager': self.min_wager,
            'nUnchosen': nUnchosen,
            'nOption1': nOption1,
            'nOption2': nOption2,
            'nLikes': nLikes,
            'pot': pot,
            'winner': self.winner
        }

    def __repr__(self):
        return f'<Bet {self.id}: {self.description[:20]}>'

