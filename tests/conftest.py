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
def sample_board():
    board = Board(title="Test Board", owner="Test Owner")
    db.session.add(board)
    db.session.commit()
    return board

@pytest.fixture
def board(app):
    # Create and commit a new Board
    new_board = Board(name="Sample Board")
    db.session.add(new_board)
    db.session.commit()

    return new_board

# @pytest.fixture
# def one_card(app, board):
#     # Create a Card associated with the board from the fixture
#     new_card = Card(message="Interior design examples", like_count=5, board_id=board.id)
#     db.session.add(new_card)
#     db.session.commit()

#     return new_card


@pytest.fixture
def one_board(app):
    new_board = Board(title="New Years Eve Vacation", owner="Bella Hilton")
    db.session.add(new_board)
    db.session.commit()
    return new_board

@pytest.fixture
def board(app):
    # Create and commit a new Board
    new_board = Board(name="Sample Board")
    db.session.add(new_board)
    db.session.commit()

    return new_board

# @pytest.fixture
# def one_card(app, board):
#     # Create a Card associated with the board fixture
#     new_card = Card(message="Interior design examples", like_count=5, board_id=board.id)
#     db.session.add(new_card)
#     db.session.commit()

#     return new_card

@pytest.fixture
def one_card(app, three_boards):
    # Create a new card and associate it with board with id=1
    new_card = Card(message="Interior design examples", like_count=5, board_id=1)
    db.session.add(new_card)
    db.session.commit()
    return new_card

# @pytest.fixture
# def one_card(app, one_board):
#     # Instead of setting board_id manually, link the card to the created board
#     new_card = Card(message="Interior design examples", like_count=5, board_id=one_board.id)
#     db.session.add(new_card)
#     db.session.commit()
#     return new_card


# @pytest.fixture
# def one_card(app):
#     valid_board_id = 1 
#     new_card = Card(message="Interior design examples", like_count=5, board_id=valid_board_id)
#     db.session.add(new_card)
#     db.session.commit()
#     return new_card

@pytest.fixture
def one_card(app):
    # Create a new Board to associate with the Card
    new_board = Board(name="Sample Board")  # Assuming `Board` is your model
    db.session.add(new_board)
    db.session.commit()  # Commit to generate the board's ID

    # Create a Card associated with the valid board_id
    new_card = Card(message="Interior design examples", like_count=5, board_id=new_board.id)
    db.session.add(new_card)
    db.session.commit()  # Commit the card

    return new_card

# def one_card(app, one_board):
#     # Associate the card with an existing board (assuming `one_board` is a fixture that creates a board)
#     new_card = Card(message="Interior design examples", like_count=5, board_id=one_board.id)
#     db.session.add(new_card)
#     db.session.commit()
#     return new_card

# @pytest.fixture
# def one_board(app):
#     board = Board(title="Test Board", owner="Test Owner")
#     db.session.add(board)
#     db.session.commit()
#     return board


# @pytest.fixture
# def three_boards(app):
#     db.session.add_all([
#         Board(title="Wyoming Winter Ski Trip", owner=""),
#         Board(title="Algerian Wedding 2024", owner=""),
#         Board(title="Portland Friends Trip", owner="")
#     ])
#     db.session.commit()

@pytest.fixture
def three_cards(app, one_board):
    cards = [
        Card(message="Card 1", like_count=3, board_id=one_board.id),
        Card(message="Card 2", like_count=7, board_id=one_board.id),
        Card(message="Card 3", like_count=0, board_id=one_board.id)
    ]
    db.session.add_all(cards)
    db.session.commit()
    return cards

@pytest.fixture
def three_boards(app):
    # Create three boards and add them to the session
    board1 = Board(title="Board 1", owner="Owner 1")
    board2 = Board(title="Board 2", owner="Owner 2")
    board3 = Board(title="Board 3", owner="Owner 3")
    
    db.session.add(board1)
    db.session.add(board2)
    db.session.add(board3)
    db.session.commit()

    # Return the list of boards for use in tests
    return [board1, board2, board3]


# @pytest.fixture
# def one_card(app):
#     new_card = Card(message="Interior design examples",
#                     like_count=5)
#     db.session.add(new_card)
#     db.session.commit()

@pytest.fixture
def one_card(app, three_boards):
    # Create a new card and associate it with the first board
    new_card = Card(
        message="Interior design examples",
        like_count=5,
        board_id=three_boards[0].id  # Associate with the first board
    )
    db.session.add(new_card)
    db.session.commit()
    return new_card


# @pytest.fixture
# def one_board_belongs_to_one_card(app, one_card, one_board):
#     board = Board.query.first()
#     card = Card.query.first()
#     card.boards.append(board)
#     db.session.commit()

@pytest.fixture
def one_card_belongs_to_one_board(app, one_card, one_board):
    board = Board.query.first()
    card = Card.query.first()
    board.cards.append(card)
    db.session.commit()

