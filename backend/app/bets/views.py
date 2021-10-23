from sqlalchemy import select
from sqlalchemy.orm import Bundle
from flask import Blueprint, request
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.bets.model import Bet
from app.users.model import User
from app import db
from app.bets.model import BetUserAssociation
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
    description = request.json.description
    b = Bet(description)
    db.session.add(b)
    db.session.commit()
    update()
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
    bet = bet.to_dict()

    stmt = select(
        Bundle("bet", Bet.id, Bet.description),
        Bundle("user", User.id)
    ).\
    join(BetUserAssociation, BetUserAssociation.bet_id == Bet.id).\
    join(User, BetUserAssociation.user_id == User.id).\
    filter(Bet.id == id)
    print(stmt)

    users = []
    for row in db.session.execute(stmt):
        users.append(row.user[0])
    bet['users'] = users
    return bet

