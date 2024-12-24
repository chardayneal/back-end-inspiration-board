from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.board import Board
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
    return board.to_dict(), 200

def validate_model(cls, model_id):

    # checks for valid input
    try: 
        model_id = int(model_id)
    except: 
        abort(make_response({"message": f"{cls.__name__} id {model_id} is invalid"}, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    # returns board with the corresponding board_id
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found."}, 404))

    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
        
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return {cls.__name__.lower(): new_model.to_dict()}, 201

