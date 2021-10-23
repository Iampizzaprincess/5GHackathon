import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize third-party
    db.init_app(app)

    from app.bets import bets_blueprint

    # Register blueprints
    app.register_blueprint(bets_blueprit, url_prefix='/bets')

    return app
    

if __name__ == '__main__':
    app = create_app(f'cotr.config.{os.getenv("APP_SETTINGS")}')
