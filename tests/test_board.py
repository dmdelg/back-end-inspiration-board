import pytest


def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_boards_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Tiger team board",
            "owner": "John Smith"
        }
    ]


def test_get_board(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Tiger team board",
        "owner": "John Smith"
    }


def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "My New Board",
        "owner": "Ann Brown"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "My New Board",
        "owner": "Ann Brown"
    }


def test_delete_board(client, one_board):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {"details": 'Board 1 "Tiger team board" successfully deleted'}

    # Check that the board was deleted
    response = client.get("/boards/1")
    assert response.status_code == 404
    response_body = response.get_json()
    assert response_body == {"message": f"Board 1 not found"}

