from app import create_app, db
from app.models.board import Board

my_app = create_app()
with my_app.app_context():
    db.session.add(Board(title="Best teem", owner="Teem Tiger"))
    db.session.add(Board(title="Rainbow teem", owner="Rainbow teem"))
    db.session.add(Board(title="Blue Ocean", owner="Blue Ocean"))
    db.session.add(Board(title="My team", owner="My team"))
   
    db.session.commit()