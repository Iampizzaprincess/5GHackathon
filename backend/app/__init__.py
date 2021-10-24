import os

from flask import Flask
from flask_sse import sse
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite+pysqlite:///{os.path.join(os.getcwd(), 'app.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config['REDIS_URL'] = 'redis://localhost'
    app.config['SECRET_KEY'] = 'sadkfoha;osidfji0[paewnfg[as'

    # Initialize third-party
    db.init_app(app)

    from app.bets import bets_blueprint
    from app.users import users_blueprint

    # Register blueprints
    app.register_blueprint(bets_blueprint, url_prefix='/bets')
    app.register_blueprint(users_blueprint, url_prefix='/users')
    app.register_blueprint(sse, url_prefix="/stream")

    return app
    
app = create_app()
