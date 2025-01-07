from app.models.board import Board
from app.db import db
import pytest

def test_post_card_ids_to_board(client, one_board, three_cards):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "A new card message",
        "like_count": 0 
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "board_id" in response_body
    assert "card" in response_body
    assert "id" in response_body["card"] 
    assert response_body == {
        "board_id": 1,
        "card": {
            "id": 4,  
            "message": "A new card message",
            "like_count": 0
        }
    }


def test_post_card_ids_to_board_already_with_boards(client, one_card_belongs_to_one_board, three_boards):
    response = client.post("/boards/1/cards", json={
        "message": "New Card Message",
        "like_count": 0
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "card" in response_body
    assert response_body["card"]["message"] == "New Card Message"
    assert response_body["card"]["like_count"] == 0

    board = db.session.get(Board, 1)
    assert len(board.cards) == 2
    assert any(card.message == "New Card Message" for card in board.cards)

# @pytest.mark.skip
def test_get_cards_for_specific_board_no_board(client):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "message": "Board 1 not found."
    }

# @pytest.mark.skip
def test_get_cards_for_specific_board_no_cards(client, one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "cards" in response_body
    assert len(response_body["cards"]) == 0
    assert response_body == {
        "id": 1,
        "title": "New Years Eve Vacation",
        "owner": "Bella Hilton",  
        "cards": []
    }

# @pytest.mark.skip
def test_get_cards_for_specific_board(client, one_card_belongs_to_one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "cards" in response_body
    assert len(response_body["cards"]) == 1
    assert response_body == {
        "id": 1,  # Include the board ID
        "title": "Board 1",
        "owner": "Owner 1",
        "cards": [
            {
                "id": 1,
                "message": "Interior design examples",
                "like_count": 5
            }
        ]
    }

# @pytest.mark.skip
def test_get_card_includes_board_id(client, one_card_belongs_to_one_board):
    response = client.get("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "card" in response_body
    assert response_body == {
        "card": {
            "id": 1,
            "message": "Interior design examples",
            "like_count": 5
        }
    }
