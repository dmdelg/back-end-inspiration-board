from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db


class Board(db.Model):
    __tablename__ = 'board'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    owner: Mapped[str] = mapped_column(nullable=False)
    cards: Mapped[list["Card"]] = relationship("Card", back_populates="board")

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            owner=self.owner
        )
    
    # from JSON to model
    @classmethod
    def from_dict(cls, board_data):
        return cls(
            title=board_data["title"],
            owner=board_data["owner"]
        )
