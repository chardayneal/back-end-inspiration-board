from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.board import Board
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

@boards_bp.get("/<board_id>")
def get_single_board(board_id):
    board = validate_model(Board, board_id)

    response = {"board": board.to_dict()}

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

