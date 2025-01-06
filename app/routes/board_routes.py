from flask import Blueprint, request, Response, make_response, abort
from app.models.board import Board
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
