from app.models.board import Board
from app.db import db
import pytest

def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_boards_one_saved_boards(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "New Years Eve Vacation",
            "owner": "Bella Hilton"
        }
    ]

def test_get_board(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "board" in response_body
    assert response_body == {
        "board": {
            "id": 1,
            "title": "New Years Eve Vacation",
            "owner": "Bella Hilton"
        },
        "cards": []
    }

def test_get_board_not_found(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"Board 1 not found."}


def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "Five Year Plan",
        "owner": "Henry Bennington",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
            "id": 1,
            "title": "Five Year Plan",
            "owner": "Henry Bennington"
        }
    }
    new_board = db.session.get(Board, 1)
    assert new_board
    assert new_board.title == "Five Year Plan"
    assert new_board.owner == "Henry Bennington"

def test_delete_board(client, one_board):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Board 1 "New Years Eve Vacation" successfully deleted'
    }
    assert db.session.get(Board, 1) is None

def test_delete_board_not_found(client):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"Board 1 not found."}
    assert Board.query.all() == []

def test_update_board(client, one_board):
    # Act
    response = client.put("/boards/1", json={
        "title": "Updated Board Title",
        "owner": "Updated Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "board" in response_body
    assert response_body == {
        "board": {
            "id": 1,
            "title": "Updated Board Title",
            "owner": "Updated Test Description"
        }
    }
    board = db.session.get(Board, 1)
    assert board.title == "Updated Board Title"
    assert board.owner == "Updated Test Description"


def test_update_board_not_found(client):
    # Act
    response = client.put("/boards/1", json={
        "title": "Updated Board Title",
        "owner": "Updated Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"Board 1 not found."}

def test_create_board_must_contain_title(client):
    # Act
    response = client.post("/boards", json={
        "owner": "Test Owner"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Board.query.all() == []


def test_create_board_must_contain_owner(client):
    # Act
    response = client.post("/boards", json={
        "title": "A Brand New Board"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Board.query.all() == []

def test_validate_model_invalid_id(client):
    # Act
    response = client.get("/boards/invalid_id")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Board id invalid_id is invalid"}
