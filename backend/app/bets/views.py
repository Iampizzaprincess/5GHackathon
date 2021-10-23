from flask import Blueprint
from app.bets.models import Bet

bets_blueprint = Blueprint(
    "bets", __name__
)

@bets_blueprint.route('/', methods=['POST']):
def create_bet():
    b = Bet("Woohoo")
    db.session.add(v)
    db.session.commit()
    return {'success': True}

@bets_blueprint.route('/<id>', methods=['GET'])
def get_bet():
    if not id:
        bets = Bet.query.all()
        return bets
    else:
        bet = Bet.query.filter_by(id=id).first()
        return bet

