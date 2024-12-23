from sqlalchemy.orm import Mapped, mapped_column,relationship
from ..db import db

class Card(db.Model):
    __tablename__ = 'card'
    card_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(nullable=False)
    likes_count: Mapped[int] = mapped_column(nullable=False)
    