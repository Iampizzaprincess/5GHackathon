from sqlalchemy import update
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
    sse.publish(d, channel=f"{user.id}")

def push_notificaiton_to_users(bet):
    bet['type'] = 'notification'
    for user in User.query.all():
        uid = user.id
        sse.publish(bet, channel=f"{uid}")

def push_bets_to_users():
    bets = _get_all()
    print(bets)
    bets['type'] = 'bets'
    for user in User.query.all():
        uid = user.id
        sse.publish(bets, channel=f"{uid}")
        print(url_for("sse.stream", channel=f"{uid}"))


@bets_blueprint.route('/', methods=['POST'])
def create():
    req_fields = ['description', 'option1', 'option2', 'min_wager']
    missing = check_req_fields(req_fields, request.form)
    if len(missing) != 0:
        return wrap_response({'error': "You're missing " + ', '.join(missing)})
    description = request.form['description']
    option1 = request.form['option1']
    option2 = request.form['option2']
    min_wager = float(request.form['min_wager'])
    b = Bet(description, option1, option2, min_wager)
    db.session.add(b)
    db.session.commit()
    print('test')
    push_bets_to_users()
    return wrap_response({'success': True})

@bets_blueprint.route('/<id>/select-option', methods=["POST"])
def select_option(id):
    req_fields = ['option', 'wager']
    missing = check_req_fields(req_fields, request.form)
    if len(missing) != 0:
        return wrap_response({'error': "You're missing " + ", ".join(missing)})
    
    new_wager = float(request.form['wager'])
    new_option = int(request.form['option'])

    if new_wager < 0:
        return wrap_response({'error': f'Wager {new_wager} cannot be less than 0'})
    
    if 0 < new_option or 2 < new_option:
        return wrap_response({'error': f'Option {new_option} is not 0, 1, or 2'})

    user_id = session['user_id']
    user = User().query.filter_by(id=user_id)
    betuser = BetUserAssociation.query.filter_by(user_id=user_id).filter_by(bet_id=id).first()
    if betuser is None:
        betuser = BetUserAssociation(id, user_id)

    if new_option == 0:
        user.credits = user.credits + betuser.wager
        betuser.wager = 0.00
    elif new_option != 0:
        user.credits  = user.credits + betuser.wager - new_wager
        betuser.wager = new_wager
    betuser.option = new_option

    db.session.add(betuser)
    db.session.add(user)
    db.session.commit(user)
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

@bets_blueprint.route('/<id>/end', methods=['POST'])
def end_bet(id):
    req_fields = ['option']
    missing = check_req_fields(req_fields, request.form)
    if len(missing) != 0:
        return wrap_response({'error': "You're missing " + ', '.join(missing)})

    option = int(request.form['option'])
    if 0 < option or 2 < option:
        return wrap_response({'error': f'Option {option} is not 0, 1, or 2'})
    
    bet = Bet.query.filter_by(id=id).first()
    bet_data = bet.to_dict()
    associations = BetUserAssociation.query.filter_by(bet_id=id)
    users = [] 
    if option == 0:
        for a in associations:
            user = User.query.filter_by(id=a.user_id)
            user.credits += a.wager
            users.append(user)
    elif option == 1:
        reward = bet_data.pot / bet_data.nOption1
        for a in associations:
            user = User.query.filter_by(id=a.user_id)
            if a.option == 1:
                user.credits += reward
                users.append(user)
            elif a.option == 2:
                user.credits -= a.wager
                users.append(user)
    elif option == 2:
        reward = bet_data.pot / bet_data.nOption2
        for a in associations:
            user = User.query.filter_by(id=a.user_id)
            if a.option == 1:
                user.credits -= a.wager
                users.append(user)
            elif a.option == 2:
                user.credits += reward
                users.append(user)

    for u in users:
        db.session.add(u)
    
    bet.winner = option           
    db.session.add(bet)

    db.session.commit()

    for u in users:
        push_credit_to_user(u)
    return wrap_response({'success': True})

def _get_all():
    bets = Bet.query.all()
    bets = {str(bet.id):bet.to_dict() for bet in bets}
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

