from flask import Blueprint, request
from flask.json import jsonify
from app.users.model import User
from app import db

users_blueprint = Blueprint(
    "users", __name__
)

@users_blueprint.route('/', methods=['POST'])
def create():
    description = request.json.description
    firstname = request.json.firstname
    lastname = request.json.lastname
    b = User(description, firstname, lastname)
    db.session.add(b)
    db.session.commit()
    return {'success': True}

@users_blueprint.route('/', methods=['GET'])
def get_all():
    users = User.query.all()
    users = [user.to_dict() for user in users]
    return jsonify(users) if users != [] else "I am empty inside"

@users_blueprint.route('/<id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return "No user for you"
    return user.to_dict()

