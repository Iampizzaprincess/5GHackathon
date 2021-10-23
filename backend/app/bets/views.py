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
    approved = request.json.approved
    b = Bet(description, approved)
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
    bet = bet.to_dict()

    stmt = select(
        BetUserAssociation.status, BetUserAssociation.like
    ).\
    join(User, BetUserAssociation.user_id == User.id).\
    filter(BetUserAssociation.bet_id == id)

    nNeutral = 0
    nFor = 0
    nAgainst = 0
    nLikes = 0
    for row in db.session.execute(stmt):
        if row.status == BetUserAssociation.NEUTRAL: nNeutral += 1
        if row.status == BetUserAssociation.FOR: nFor += 1
        if row.status == BetUserAssociation.AGAINST: nAgainst += 1
        if row.like : nLikes += 1

    bet['neutral'] = nNeutral
    bet['for'] = nFor
    bet['against'] = nAgainst
    bet['likes'] = nLikes
    return bet

