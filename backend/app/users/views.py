from flask import Blueprint, request, session
from app.util import wrap_response
from app.users.model import User
from app import db
import string
import random

users_blueprint = Blueprint(
    "users", __name__
)

@users_blueprint.route('/login', methods=['POST'])
def login():
    username = ''.join(random.choice(string.ascii_letters) for i in range(10))
    firstname = request.json.get('name')
    lastname = firstname
    u = User(username, firstname, lastname, 100.0)
    db.session.add(u)
    db.session.commit()
    u = User.query.filter_by(username=username).first()
    session['user_id'] = u.id
    return wrap_response({'success': True, 'id':u.id})

@users_blueprint.route('/', methods=['GET'])
def get_all():
    users = User.query.all()
    users = {i:user.to_dict() for i,user in enumerate(users)}
    return wrap_response(users)

@users_blueprint.route('/<id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return wrap_response("No user for you")
    return wrap_response(user.to_dict())

