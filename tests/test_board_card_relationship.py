from app.models.card import Card
import pytest


def test_post_board_ids_to_card(client, one_card, three_boards):
    # Act
    response = client.post("/cards/1/boards", json={
        "board_ids": [1, 2, 3]
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "id" in response_body
    assert "board_ids" in response_body
    assert response_body == {
        "id": 1,
        "board_ids": [1, 2, 3]
    }

    # Check that Card was updated in the db
    assert len(Card.query.get(1).boards) == 3


def test_post_board_ids_to_card_already_with_cards(client, one_board_belongs_to_one_card, three_boards):
    # Act
    response = client.post("/cards/1/boards", json={
        "board_ids": [1, 4]
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "id" in response_body
    assert "board_ids" in response_body
    assert response_body == {
        "id": 1,
        "board_ids": [1, 4]
    }
    assert len(Card.query.get(1).boards) == 2


def test_get_boards_for_specific_card_no_card(client):
    # Act
    response = client.get("/cards/1/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "message": "Card 1 not found."
    }


def test_get_boards_for_specific_card_no_boards(client, one_card):
    # Act
    response = client.get("/cards/1/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "boards" in response_body
    assert len(response_body["boards"]) == 0
    assert response_body == {
        "id": 1,
        "message": "Interior design examples",
        "like_count": 5,
        "boards": []
    }


def test_get_boards_for_specific_card(client, one_board_belongs_to_one_card):
    # Act
    response = client.get("/cards/1/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "boards" in response_body
    assert len(response_body["boards"]) == 1
    assert response_body == {
        "id": 1,
        "message": "Interior design examples",
        "like_count": 5,
        "boards": [
            {
                "id": 1,
                # "card_id": 1,
                "title": "New Years Eve Vacation",
                "owner": "Bella Hilton"
            }
        ]
    }


def test_get_board_includes_card_id(client, one_board_belongs_to_one_card):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "board" in response_body
    # assert "card_id" in response_body["board"]
    assert response_body == {
        "board": {
            "id": 1,
            # "card_id": 1,
            "title": "New Years Eve Vacation",
            "owner": "Bella Hilton"
        }
    }
