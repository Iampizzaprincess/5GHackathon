from flask import Blueprint, request
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.bets.model import Bet
from app import db
from app import sse
import datetime


bets_blueprint = Blueprint(
    "bets", __name__
    )

@bets_blueprint.route('/sseupdate')
def update():
    sse.publish(get_all())
    return f"pushed update of all bets at {datetime.datetime.now()}"

@bets_blueprint.route('/', methods=['POST'])
def create():
    b = Bet("Woohoo")
    db.session.add(b)
    db.session.commit()
    return {'success': True}

@bets_blueprint.route('/', methods=['GET'])
def get_all():
    bets = Bet.query.all()
    bets = {i:bet for i,bet in enumerate(bets)}
    return bets if bets != {} else "I am empty inside"

@bets_blueprint.route('/<id>', methods=['GET'])
def get_bet(id):
    bet = Bet.query.filter_by(id=id).first()
    if bet is None:
        return "Fuck you"
    return bet

