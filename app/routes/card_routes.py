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

@cards_bp.patch("/<card_id>/like")
def like_card(card_id):
    card = validate_model(Card, card_id)
    card.like_count += 1
    
    return card.to_dict(), 200
