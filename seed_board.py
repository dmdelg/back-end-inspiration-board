from app import create_app, db
from app.models.board import Board

my_app = create_app()
with my_app.app_context():
    db.session.add(Board(title="Best team", owner="Team Tiger"))
    db.session.add(Board(title="Rainbow team", owner="Rainbow team"))
    db.session.add(Board(title="Blue Ocean", owner="Blue Ocean"))
    db.session.add(Board(title="My team", owner="My team"))
   
    db.session.commit()