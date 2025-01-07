from flask import Flask
from .db import db, migrate
import os
from .models import board, card
from flask_cors import CORS
from .routes.board_routes import bp as board_bp
from .routes.card_routes import bp as card_bp


def create_app(config=None):
    app = Flask(__name__)

    # Set default configuration
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # Update with test or custom configuration if provided
    if config:
        app.config.update(config)

    # Initialize app with SQLAlchemy db and Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models to register them with SQLAlchemy
    with app.app_context():
        from .models.board import Board
        from .models.card import Card

    # Register Blueprints
    app.register_blueprint(board_bp)
    app.register_blueprint(card_bp)

    # Enable Cross-Origin Resource Sharing
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    return app
