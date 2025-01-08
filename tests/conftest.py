import pytest
from flask import Flask
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.card import Card
from app.models.board import Board
from datetime import datetime


load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# This fixture gets called in every test that
# references "one_board"
# This fixture creates a board and saves it in the database
@pytest.fixture
def one_board(app):
    new_board = Board(title="Tiger team board", owner="John Smith")
    db.session.add(new_board)
    db.session.commit()
    return new_board

# This fixture gets called in every test that
# references "one_card_belongs_to_one_board"
# This fixture creates a card and a board
# It associates the board and card, so that the
# board has this card, and the card belongs to one board
@pytest.fixture
def one_card_belongs_to_one_board(app, one_board):
    card = Card(message="Test Card", board_id=Board.query.first().id)
    db.session.add(card)
    db.session.commit()
    return card
