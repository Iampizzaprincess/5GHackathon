from flask import Blueprint

bets_blueprint = Blueprint(
    "bets", __name__
)

from app.bets.views import *
