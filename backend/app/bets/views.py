from sqlalchemy import select
from sqlalchemy.orm import Bundle
from flask import Blueprint, request, make_response
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

def check_req_fields(fields, obj):
    missing = [i for i, field in enumerate(fields) if field not in obj]
    return missing

def wrap_response(package):
    resp = make_response(package)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp


@bets_blueprint.route('/sseupdate')
def update():
    sse.publish(get_all())
    return wrap_response(f"pushed update of all bets at {datetime.datetime.now()}")

@bets_blueprint.route('/', methods=['POST'])
def create():
    req_fields = ['description', 'approved', 'option1', 'option2']
    missing = check_req_fields(req_fields, request.json)
    if len(missing) != 0:
        return wrap_response("You're missing " + ', '.join(missing))
    description = request.json.description
    approved = request.json.approved
    option1 = request.json.option1
    option2 = request.json.option2
    b = Bet(description, approved, option1, option2)
    db.session.add(b)
    db.session.commit()
    update()
    return wrap_response({'success': True})

@bets_blueprint.route('/', methods=['GET'])
def get_all():
    bets = Bet.query.all()
    bets = {bet.id:bet.to_dict() for bet in bets}
    return wrap_response(bets if bets != {} else "I am empty inside")

@bets_blueprint.route('/<id>', methods=['GET'])
def get_bet(id):        
    bet = Bet.query.filter_by(id=id).first()
    if bet is None:
        return wrap_response("No bet for you")
    bet = bet.to_dict()

    stmt = select(
        BetUserAssociation.decision, BetUserAssociation.like
    ).\
    join(User, BetUserAssociation.user_id == User.id).\
    filter(BetUserAssociation.bet_id == id)

    nUndecided = 0
    nOption1 = 0
    nOption2 = 0
    nLikes = 0
    for row in db.session.execute(stmt):
        if row.decision == BetUserAssociation.UNDECIDED: nUndecided += 1
        if row.decision == BetUserAssociation.OPTION1: nOption1 += 1
        if row.decision == BetUserAssociation.OPTION2: nOption2 += 1
        if row.like : nLikes += 1

    bet['nUndecided'] = nUndecided
    bet['nOption1'] = nOption1
    bet['nOption2'] = nOption2
    bet['nLikes'] = nLikes
    return wrap_response(bet)

