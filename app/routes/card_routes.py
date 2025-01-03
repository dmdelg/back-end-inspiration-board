from flask import Blueprint, request
from ..db import db
<<<<<<< HEAD
from app.models.board import Board
from app.models.card import Card
=======
from app.models.card import Card
from app.models.board import Board
>>>>>>> f37d71c42b1aa84d031447189c9d6d96a24428f9

bp = Blueprint('cards', __name__, url_prefix='/cards')

@bp.route('/', methods=['POST'])
def create_card():
    data = request.get_json()
    message = data.get('message')
    board_id = data.get('board_id')

    if not message or not board_id:
        return {"error": 'Both "message" and "board_id" are required'}, 400

    board = Board.query.get(board_id)
    if not board:
        return {"error": "Board not found"}, 404

    card = Card(message=message, likes=0, board_id=board_id)
    db.session.add(card)
    db.session.commit()

    return {
        "id": card.id,
        "message": card.message,
        "likes": card.likes,
        "board_id": card.board_id
    }, 201

@bp.route('/', methods=['GET'])
def get_cards():
    board_id = request.args.get('board_id')
    if board_id:
        cards = Card.query.filter_by(board_id=board_id).all()
    else:
        cards = Card.query.all()

    return [
        {
            "id": card.id,
            "message": card.message,
            "likes": card.likes,
            "board_id": card.board_id
        }
        for card in cards
    ], 200





