import pytest
from app.models.board import Board
from app.models.card import Card
from app.db import db

def test_create_card(client, one_board):
    # Act
    response = client.post("/cards", json={
        "message": "New Card for Board",
        "board_id": one_board.id
    })
    response_body = response.get_json()

    #Assert
    assert response.status_code == 201
    assert response_body["message"] == "New Card for Board"
    assert response_body["board_id"] == 1

def test_create_card_missing_fields(client):
    # Act
    response = client.post("/cards", json={"message": "Missing board_id"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["error"] == 'Both "message" and "board_id" are required'

def test_create_card_board_not_found(client):
    # Act
    response = client.post("/cards", json={
        "message": "Card for Non-existent Board",
        "board_id": 9999
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body["error"] == "Board not found"

def test_get_cards(client, one_card_belongs_to_one_board):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["message"] == "Test Card"

def test_get_card(client, one_card_belongs_to_one_board):
    # Act
    response = client.get(f"/cards/{one_card_belongs_to_one_board.id}")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["id"] == one_card_belongs_to_one_board.id
    assert response_body["message"] == "Test Card"

def test_get_card_not_found(client):
    # Act
    response = client.get("/cards/9999")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body["message"] == "Card 9999 not found"

def test_delete_card(client, one_card_belongs_to_one_board):
    # Act
    response = client.delete(f"/cards/{one_card_belongs_to_one_board.id}")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["details"] == f'Card {one_card_belongs_to_one_board.id} "Test Card" successfully deleted'

    response = client.get(f"/cards/{one_card_belongs_to_one_board.id}")
    assert response.status_code == 404
    response_body = response.get_json()
    assert response_body["message"] == f"Card {one_card_belongs_to_one_board.id} not found"

def test_update_card_like_success(client, app, one_board):
    new_card = {
        "message": "Test card",
        "likes": 0,
        "board_id": one_board.id,
    }
    response = client.post("/cards", json=new_card)
    assert response.status_code == 201
    response_body = response.get_json()
    card_id = response_body["id"]

    response = client.patch(f"/cards/{card_id}/like")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["card"]["id"] == card_id
    assert response_body["card"]["likes"] == 1

    with app.app_context():
        updated_card = Card.query.get(card_id)
        assert updated_card is not None
        assert updated_card.likes == 1

def test_update_card_like_not_found(client):
    # Act:
    response = client.patch("/cards/1/like")
    # Assert:
    assert response.status_code == 404
    response_body = response.get_json()
    assert response_body["message"] == "Card 1 not found"