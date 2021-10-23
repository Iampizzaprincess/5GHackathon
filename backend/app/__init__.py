import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite+pysqlite:///{os.path.join(os.getcwd(), 'app.db')}"

    # Initialize third-party
    db.init_app(app)

    from app.bets import bets_blueprint

    # Register blueprints
    app.register_blueprint(bets_blueprint, url_prefix='/bets')

    return app
    
app = create_app()
