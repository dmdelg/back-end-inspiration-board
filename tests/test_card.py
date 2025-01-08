import pytest

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
    assert response_body["board_id"] == one_board.id

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
    assert "cards" in response_body  
    assert len(response_body["cards"]) == 1  
    assert response_body["cards"][0]["message"] == "Test Card" 

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
