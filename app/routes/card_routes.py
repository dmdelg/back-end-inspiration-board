from flask import Blueprint, request, Response, make_response, abort
from ..db import db
from app.models.board import Board
from app.models.card import Card

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

@bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_card(card_id)
    db.session.delete(card)
    db.session.commit()

    response = {
        "details": f"Card {card_id} \"{card.title}\" successfully deleted"
    }

    return response, 200

def validate_card(card_id):
    try:
        card_id = int(card_id)
    except:
        response = {"details": "Invalid data"}

        abort(make_response(response , 400))

    query = db.select(Card).where(Card.id == card_id)
    card = db.session.scalar(query)
    
    if not card:
        response = {"message": f"task {card_id} not found"}
        abort(make_response(response, 404))

    return card



