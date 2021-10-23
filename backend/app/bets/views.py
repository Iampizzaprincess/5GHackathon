from flask import Blueprint, request
from app.bets.model import Bet
from app import db

bets_blueprint = Blueprint(
    "bets", __name__
)

@bets_blueprint.route('/', methods=['POST'])
def create():
    b = Bet("Woohoo")
    db.session.add(b)
    db.session.commit()
    return {'success': True}

@bets_blueprint.route('/', methods=['GET'])
def get_all():
    bets = Bet.query.all()
    bets = {bet.id:bet.to_dict() for bet in bets}
    return bets if bets != {} else "I am empty inside"

@bets_blueprint.route('/<id>', methods=['GET'])
def get_bet(id):
    bet = Bet.query.filter_by(id=id).first()
    if bet is None:
        return "No bet for you"
    return bet.to_dict()

