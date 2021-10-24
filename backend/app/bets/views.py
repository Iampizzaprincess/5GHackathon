from sqlalchemy import select
from sqlalchemy.orm import Bundle
from flask import Blueprint, request, session, url_for
import datetime
from app.bets.model import Bet
from app.users.model import User
from app import db
from app.bets.model import BetUserAssociation
from app import sse
from app.util import check_req_fields, wrap_response
import datetime

bets_blueprint = Blueprint(
    "bets", __name__
)

@bets_blueprint.route('/sseupdate')
def update():
    sse.publish(_get_all())

#def push_betstats_to_user() TODO : betstats

def push_credit_to_user(user):
    d = {}
    d['type'] = 'credit'
    d['credits'] = user.credits
    resp = wrap_response(d)
    sse.publish(resp, channel=f"{d}")

def push_notificaiton_to_users(bet):
    bet['type'] = 'notification'
    resp = wrap_response(bet)
    for user in User.query.all():
        uid = user.id
        sse.publish(resp, channel=f"{uid}")

def push_bets_to_users():
    bets = {bet.id:bet.to_dict() for bet in bets}
    bets['type'] = 'bets'
    resp = wrap_response(bets)
    for user in User.query.all():
        uid = user.id
        sse.publish(resp, channel=f"{uid}")
        print(url_for("stream", channel=f"{uid}"))


@bets_blueprint.route('/', methods=['POST'])
def create():
    req_fields = ['description', 'option1', 'option2', 'min_wager']
    missing = check_req_fields(req_fields, request.json)
    if len(missing) != 0:
        return wrap_response({'error': "You're missing " + ', '.join(missing)})
    description = request.json['description']
    option1 = request.json['option1']
    option2 = request.json['option2']
    min_wager = float(request.json['min_wager'])
    b = Bet(description, option1, option2, min_wager)
    db.session.add(b)
    db.session.commit()
    push_bets_to_users()
    return wrap_response({'success': True})

@bets_blueprint.route('/<id>/select-option', methods=["POST"])
def select_option(id):
    req_fields = ['option', 'wager']
    missing = check_req_fields(req_fields, request.json)
    if len(missing) != 0:
        return wrap_response({'error': "You're missing " + ", ".join(missing)})
    user_id = session['user_id']
    betuser = BetUserAssociation.query.filter_by(user_id=user_id).filter_by(bet_id=id).first()
    if betuser is None:
        betuser = BetUserAssociation(id, user_id)
    betuser.option = int(request.json['option'])
    betuser.wager = float(request.json['wager'])
    db.session.add(betuser)
    db.session.commit(betuser)
    return wrap_response({'success': True})

@bets_blueprint.route('/<id>/approve', methods=['POST'])
def set_id_approve(id):
    bet = Bet.query.filter_by(id=id).first()
    if bet is None:
        return wrap_response({"success" : False})
    bet.approved = True
    db.session.add(bet)
    db.session.commit()
    return wrap_response({'success':True})

@bets_blueprint.route('/<id>/unapprove', methods=['POST'])
def set_id_unapprove(id):
    bet = Bet.query.filter_by(id=id).first()
    if bet is None:
        return wrap_response({"success" : False})
    bet.approved = False
    db.session.add(bet)
    db.session.commit()
    return wrap_response({'success':True})

@bets_blueprint.route('/<id>/like', methods=['POST'])
def set_id_like(id):
    betuser = BetUserAssociation.query.filter_by(user_id=session['user_id']).filter_by(bet_id=id).first() 
    if betuser is None:
        betuser = BetUserAssociation(id, session['user_id'])
    betuser.like = True
    db.session.add(betuser)
    db.session.commit()
    return wrap_response({'success': True})
    
@bets_blueprint.route('/<id>/unlike', methods=['POST'])
def set_id_unike(id):
    betuser = BetUserAssociation.query.filter_by(user_id=session['user_id']).filter_by(bet_id=id).first() 
    if betuser is None:
        betuser = BetUserAssociation(id, session['user_id'])
    betuser.like = False
    db.session.add(betuser)
    db.session.commit()
    return wrap_response({'success': True})

def _get_all():
    bets = Bet.query.all()
    bets = {bet.id:bet.to_dict() for bet in bets}
    return bets

@bets_blueprint.route('/', methods=['GET'])
def get_all():
    return wrap_response(_get_all())

@bets_blueprint.route('/<id>', methods=['GET'])
def get_bet(id):
    bet = Bet.query.filter_by(id=id).first()
    if bet is None:
        return wrap_response({"success" : False})
    bet = bet.to_dict()
    return wrap_response(bet)

