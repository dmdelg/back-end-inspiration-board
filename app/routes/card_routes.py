from flask import Blueprint, request, Response, make_response, abort
from app.models.card import Card
from app.models.board import Board
from ..db import db

bp = Blueprint('cards', __name__, url_prefix='/cards')

@bp.post("")
def create_card():
    data = request.get_json()

    message = data.get('message')
    board_id = data.get('board_id')

    if not message or not board_id:
        response = {"error": 'Both "message" and "board_id" are required'}
        return make_response(response, 400)

    query = db.select(Board).where(Board.id == board_id)
    board = db.session.scalar(query)

    if not board:
        response = {"error": "Board not found"}
        return make_response(response, 404)

    card = Card(message=message, likes=0, board_id=board_id)
    db.session.add(card)
    db.session.commit()

    return {
        "id": card.id,
        "message": card.message,
        "likes": card.likes,
        "board_id": card.board_id
    }, 201

@bp.get("")
def get_cards():
    board_id = request.args.get('board_id')
    query = db.select(Card)

    if board_id:
        query = query.where(Card.board_id == board_id)

    cards = db.session.scalars(query)

    cards_response = [
        {
            "id": card.id,
            "message": card.message,
            "likes": card.likes,
            "board_id": card.board_id
        }
        for card in cards
    ]

    return cards_response, 200

@bp.get("/<card_id>")
def get_one_card(card_id):
    card = validate_card(card_id)

    return {
        "id": card.id,
        "message": card.message,
        "likes": card.likes,
        "board_id": card.board_id
    }, 200

@bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_card(card_id)
    db.session.delete(card)
    db.session.commit()

    response = {
        "details": f"Card {card_id} \"{card.message}\" successfully deleted"
    }

    return response, 200

def validate_card(card_id):
    try:
        card_id = int(card_id)
    except ValueError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    query = db.select(Card).where(Card.id == card_id)
    card = db.session.scalar(query)
    
    if not card:
        response = {"message": f"Card {card_id} not found"}
        abort(make_response(response, 404))

    return card



