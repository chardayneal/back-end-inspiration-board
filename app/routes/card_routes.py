from flask import Blueprint, request, make_response, abort
from app.models.card import Card
from app.models.board import Board
from ..db import db
from .route_utilities import validate_model, create_model
import requests
import os
# from .route_utilities import validate_model

cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@cards_bp.post("")
def create_card():
    request_body = request.get_json()

    return create_model(Card, request_body)

@cards_bp.get("")
def get_all_cards():
    query = db.select(Card).order_by(Card.id)
    cards = db.session.scalars(query)

    response=[card.to_dict() for card in cards]

    return response, 200

@cards_bp.get("/<card_id>")
def get_single_card(card_id):
    card = validate_model(Card, card_id)

    response = {"card": card.to_dict()}

    return response, 200

@cards_bp.put("/<card_id>")
def update_card(card_id):
    card = validate_model(Card, card_id)

    request_body = request.get_json()
    card.message = request_body["message"]
    card.like_count = request_body["like_count"]

    db.session.commit()
    response = {"card": card.to_dict()}

    return response, 200

@cards_bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_model(Card, card_id)
    db.session.delete(card)

    db.session.commit()
    response = {"details": f"Card {card.id} \"{card.message}\" successfully deleted"}

    return response, 200

@cards_bp.post("/<card_id>/boards")
def create_board_ids_by_card(card_id):
    request_body = request.get_json()
    card = validate_model(Card, card_id)

    try:
        board_ids = request_body["board_ids"]
        for board_id in board_ids:
            board = validate_model(Board, board_id)
            card.boards.append(board)
        db.session.commit()
        
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    return {"id": card.id, "board_ids": board_ids}

@cards_bp.get("/<card_id>/boards")
def get_boards_by_card(card_id):
    card = validate_model(Card, card_id)
    card_dict = card.to_dict()
    card_dict["boards"] = []

    for board in card.boards:
        card_dict["boards"].append(board.to_dict())

    return card_dict
