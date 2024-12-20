from sqlalchemy.orm import Mapped, mapped_column,relationship
from ..db import db

class Board(db.Model):
    __tablename__ = 'board'
    board_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    owner: Mapped[str] = mapped_column(nullable=False)
    