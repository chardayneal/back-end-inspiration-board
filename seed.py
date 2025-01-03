from app import create_app, db
from app.models.board import Board

my_app = create_app()
with my_app.app_context():

    # seeds data into Board table
    db.session.add(Board(title="Dream Big", owner="Alice"))
    db.session.add(Board(title="Adventure Awaits", owner="Bob"))
    db.session.add(Board(title="Chasing Goals", owner="Charlie"))
    db.session.add(Board(title="Moments of Joy", owner="David"))
    db.session.add(Board(title="Strength and Growth", owner="Eve"))
    db.session.add(Board(title="Pages of Inspiration", owner="Frank"))
    db.session.add(Board(title="Wanderlust Dreams", owner="Grace"))
    db.session.add(Board(title="Sparkling Clean", owner="Hannah"))
    db.session.add(Board(title="Balanced Living", owner="Ivy"))
    db.session.add(Board(title="Flavors of Love", owner="Jack"))
    db.session.add(Board(title="Harmony at Home", owner="Kim"))

    # seeds data into Card table
    db.session.add(Card(message="Dream Big", like_count=12))
    db.session.add(Card(message="Adventure Awaits", like_count=45))
    db.session.add(Card(message="Chasing Goals", like_count=30))
    db.session.add(Card(message="Moments of Joy", like_count=67))
    db.session.add(Card(message="Strength and Growth", like_count=23))
    db.session.add(Card(message="Pages of Inspiration", like_count=56))
    db.session.add(Card(message="Wanderlust Dreams", like_count=89))
    db.session.add(Card(message="Sparkling Clean", like_count=34))
    db.session.add(Card(message="Balanced Living", like_count=50))
    db.session.add(Card(message="Flavors of Love", like_count=76))
    db.session.add(Card(message="Harmony at Home", like_count=41))



    db.session.commit()