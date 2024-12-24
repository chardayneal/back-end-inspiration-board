from flask import abort, make_response
from ..db import db
from ..models.board import Board
# from ..models.card import Card
# from sqlalchemy import desc, asc

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

    response = {cls.__name__.lower(): new_model.to_dict()}

    return response, 201