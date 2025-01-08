from flask import Blueprint, request, Response, make_response, abort
from app.models.board import Board
from app.models.card import Card
from ..db import db

bp = Blueprint("board_bp", __name__, url_prefix="/boards")

@bp.post("")
def create_board():
    request_body = request.get_json()

    try:
        new_board = Board.from_dict(request_body)

    except KeyError as e:
        print(e)
        response = {
            "details": "Invalid data"
        }
        abort(make_response(response, 400))

    db.session.add(new_board)
    db.session.commit()

    return new_board.to_dict(), 201

@bp.get("")
def get_all_boards():
    query = db.select(Board)
    query = query.order_by(Board.id)
    boards = db.session.scalars(query)

    boards_response = []
    for board in boards:
        boards_response.append(
            {
                "id": board.id,
                "title": board.title,
                "owner": board.owner
            }
        )

    return boards_response

@bp.get("/<board_id>")
def get_one_board(board_id):
    board = validate_board(board_id)

    return board.to_dict()

@bp.delete("/<board_id>")
def delete_board(board_id):
    board = validate_board(board_id)
    
    for card in board.cards:
        db.session.delete(card)

    db.session.delete(board)
    db.session.commit()

    response = {
        "details": f"Board {board_id} \"{board.title}\" successfully deleted"
    }

    return response, 200


@bp.delete("")
def delete_all_boards():
    query = db.select(Board)
    boards = db.session.scalars(query)

    for board in boards:

        for card in board.cards:
            db.session.delete(card)

        db.session.delete(board)
    
    db.session.commit()

    response = {
        "details": f"All boards deleted successfully"
    }

    return response, 200


@bp.post("/<board_id>/cards")
def create_card_to_board(board_id):
    board = validate_board(board_id)
    
    request_body = request.get_json()
    message = request_body["message"]
    if "message" not in request_body:
        request_body = {"details": "Card message is required"}
        return make_response(response_body, 400)

    new_card = Card(message=message, board=board)
    db.session.add(new_card)
    db.session.commit()
    
    response_body = new_card.to_dict()
    
    return response_body, 201


@bp.get("/<board_id>/cards")
def get_cards_for_board(board_id):
    board = validate_board(board_id)
    cards = db.session.query(Card).filter_by(board_id=board.id).order_by(Card.id).all()

    cards_response = []
    for card in cards:
        cards_response.append(
            {
                "id": card.id,
                "message": card.message,
                "board_id": card.board_id,
            }
        )

    return cards_response
    

def validate_board(board_id):
    try:
        board_id = int(board_id)
    except:
        response = {"details": "Invalid data"}

        abort(make_response(response , 400))

    query = db.select(Board).where(Board.id == board_id)
    board = db.session.scalar(query)
    
    if not board:
        response = {"message": f"Board {board_id} not found"}
        abort(make_response(response, 404))

    return board
