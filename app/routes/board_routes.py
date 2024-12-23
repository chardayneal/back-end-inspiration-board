from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.board import Board
import requests
import os

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@boards_bp.post("")
def create_board():
    request_body = request.get_json()
    title = request_body["title"]
    owner = request_body["owner"]

    new_board = Board(title=title, owner=owner)
    db.session.add(new_board)
    db.session.commit()
    response = new_board.to_dict()
    return response, 201

@boards_bp.get("")
def get_all_boards():
    query = db.select(Board).order_by(Board.title)
    boards = db.session.scalars(query)

    results_list = []
    results_list = [board.to_dict() for board in boards]
    return results_list

@boards_bp.get("/<board_id>")
def get_one_board(board_id):
    board = validate_board(board_id)
    return board.to_dict(), 200

def validate_board(board_id):

    # checks for valid input
    try: 
        board_id = int(board_id)
    except: 
        abort(make_response({"message": f"Board id {board_id} not found"}, 400))

    board = Board.query.get(board_id)
    # returns task with the corresponding task_id
    if not board:
        abort(make_response({"message": f"Board id {board_id} not found"}, 404))

    return board
