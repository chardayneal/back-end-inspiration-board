from app import create_app, db
from app.models.board import Board

my_app = create_app()
with my_app.app_context():
    db.session.add(Board(title="Do laundry", owner="Alice"))
    db.session.add(Board(title="Buy groceries", owner="Bob"))
    db.session.add(Board(title="Prepare presentation", owner="Charlie"))
    db.session.add(Board(title="Call the plumber", owner="David"))
    db.session.add(Board(title="Workout", owner="Eve"))
    db.session.add(Board(title="Finish book", owner="Frank"))
    db.session.add(Board(title="Plan trip", owner="Grace"))
    db.session.add(Board(title="Clean the car", owner="Hannah"))
    db.session.add(Board(title="Pay utility bills", owner="Ivy"))
    db.session.add(Board(title="Cook a special dinner", owner="Jack"))
    db.session.add(Board(title="Organize the closet", owner="Kim"))
    db.session.commit()