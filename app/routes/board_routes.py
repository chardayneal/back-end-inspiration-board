from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.board import Board
from ..models.card import Card
from .route_utilities import validate_model, create_model
import requests
import os

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@boards_bp.post("")
def create_board():
    request_body = request.get_json()

    return create_model(Board, request_body)

@boards_bp.get("")
def get_all_boards():
    query = db.select(Board).order_by(Board.title)
    boards = db.session.scalars(query)

    results_list = []
    results_list = [board.to_dict() for board in boards]

    return results_list

# @boards_bp.get("/<board_id>")
# def get_single_board(board_id):
#     board = validate_model(Board, board_id)

#     response = {"board": board.to_dict()}

#     return response, 200

@boards_bp.get("/<board_id>")
def get_single_board(board_id):
    board = validate_model(Board, board_id)

    response = {
        "board": board.to_dict(),
        "cards": [card.to_dict() for card in board.cards]
    }

    return response, 200

@boards_bp.put("/<board_id>")
def update_board(board_id):
    board = validate_model(Board, board_id)

    request_body = request.get_json()
    board.title = request_body["title"]
    board.owner = request_body["owner"]

    db.session.commit()

    return {"board": board.to_dict()}

@boards_bp.delete("/<board_id>")
def delete_board(board_id):
    board = validate_model(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    response = {"details": f"Board {board_id} \"{board.title}\" successfully deleted"}

    return response


@boards_bp.post("/<board_id>/cards")
def create_card_for_board(board_id):
    board = validate_model(Board, board_id) 
    request_body = request.get_json()

    try:
        new_card = Card(
            message=request_body["message"],
            like_count=request_body.get("like_count", 0),
            board_id=board.id
        )

        db.session.add(new_card)
        db.session.commit()


        return {
            "card": new_card.to_dict(),
            "board_id": board.id
        }, 201

    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

@boards_bp.get("/<board_id>/cards")
def get_cards_by_board(board_id):
    board = validate_model(Board, board_id)
  
    response_body = {
        "id": board.id,  # Add this line to include the board ID
        "title": board.title,
        "owner": board.owner,
        "cards": [
            {
                "id": card.id,
                "message": card.message,
                "like_count": card.like_count,
            }
            for card in board.cards
        ],
    }

    return response_body, 200