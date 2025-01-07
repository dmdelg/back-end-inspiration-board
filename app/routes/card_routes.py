from flask import Blueprint, request, Response, make_response, abort
from app.models.card import Card
from app.models.board import Board
from ..db import db

bp = Blueprint('cards', __name__, url_prefix='/cards')

@bp.post("")
def create_card():
    data = request.get_json()
    message = data.get("message")
    board_id = data.get("board_id")

    if not message or not board_id:
        return {"error": 'Both "message" and "board_id" are required'}, 400

    board = db.session.get(Board, board_id)
    if not board:
        return {"error": "Board not found"}, 404

    card = Card(message=message, board_id=board_id)
    db.session.add(card)
    db.session.commit()

    return {"message": card.message, "board_id": card.board_id}, 201

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

    # Return a dictionary for consistency
    return {"cards": cards_response}, 200

@bp.get("/<card_id>")
def get_card(card_id):
    card = Card.query.get(card_id)
    
    if card is None:
        return {"message": f"Card {card_id} not found"}, 404
    
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
    
    return {
        "details": f'Card {card_id} "{card.message}" successfully deleted'
    }, 200

@bp.put("/<card_id>/like")
def update_card_like(card_id):
    card = validate_card(card_id)

    # Increment the likes count
    card.likes += 1
    db.session.commit()

    return {
        "id": card.id,
        "message": card.message,
        "likes": card.likes,
        "board_id": card.board_id
    }, 200

def validate_card(card_id):
    try:
        card_id = int(card_id)
    except ValueError:
        response = {"error": "Invalid card ID"}
        abort(make_response(response, 400)) 

    card = Card.query.get(card_id)
    if not card:
        response = {"error": f"Card {card_id} not found"}
        abort(make_response(response, 404))

    return card