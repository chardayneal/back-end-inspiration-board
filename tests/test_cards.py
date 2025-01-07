
from app.models.card import Card
from app.db import db
import pytest


def test_get_cards_no_saved_cards(client):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_cards_one_saved_card(client, one_card):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "message": "Interior design examples",
            "like_count": 5
        }
    ]


# @pytest.mark.skip

def test_get_card(client, one_card):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "card" in response_body
    assert response_body == {
        "card": {
            "id": 1,
            "message": "Interior design examples",
            "like_count": 5
        }
    }


def test_get_card_not_found(client):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"Card 1 not found."}



def test_create_card(client, one_board):
    board_id = one_board.id

    # Act
    response = client.post(f'/boards/{board_id}/cards', json={
        "message": "My New Card",
        "like_count": 5,
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "card" in response_body
    assert response_body == {
        "card": {
            "id": 1,
            "message": "My New Card",
            "like_count": 5
        },
        "board_id": 1
    }



def test_update_card(client, one_card):
    # Act
    response = client.put("/cards/1", json={"message": "Updated Card Message", "like_count": 2})
    response_body = response.get_json()
    # updated_card = Card.query.get(1)

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "card": {
            "id": 1,
            "message": "Updated Card Message",
            "like_count": 2
        }
    }
    card = Card.query.get(1)
    assert card.message == "Updated Card Message"
    assert card.like_count == 2



def test_update_card_not_found(client):
    # Act
    response = client.put("/cards/1", json={"message": "Updated Card Message"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"Card 1 not found."}


def test_delete_card(client, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Card 1 "Interior design examples" successfully deleted'
    }

    response = client.get("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message":"Card 1 not found."}



def test_delete_card_not_found(client):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"Card 1 not found."}



def test_create_card_missing_message(client):
    # Act
    response = client.post("/cards", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }
