import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.board import Board
from app.models.card import Card

load_dotenv()

@pytest.fixture
def app():
    # create the app with a test configuration
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def one_board(app):
    new_board = Board(title="New Years Eve Vacation", 
                    owner="Bella Hilton")
    db.session.add(new_board)
    db.session.commit()


@pytest.fixture
def three_boards(app):
    db.session.add_all([
        Board(title="Wyoming Winter Ski Trip", owner=""),
        Board(title="Algerian Wedding 2024", owner=""),
        Board(title="Portland Friends Trip", owner="")
    ])
    db.session.commit()


@pytest.fixture
def one_card(app):
    new_card = Card(message="Interior design examples",
                    like_count=5)
    db.session.add(new_card)
    db.session.commit()


@pytest.fixture
def one_board_belongs_to_one_card(app, one_card, one_board):
    board = Board.query.first()
    card = Card.query.first()
    card.boards.append(board)
    db.session.commit()
