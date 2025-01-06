from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from .board import Board
from ..db import db

class Card(db.Model):
    __tablename__ = 'card'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(nullable=False)
    likes: Mapped[int] = mapped_column(default = 0, nullable=False)
    board_id: Mapped[int] = mapped_column(Integer, ForeignKey('board.id'), nullable=False)

    board: Mapped['Board'] = relationship('Board', back_populates='cards')
