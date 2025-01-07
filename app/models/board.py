from ..db import db 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional

class Board(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] 
    owner: Mapped[str]
    cards: Mapped[list["Card"]] = relationship("Card", back_populates="board", cascade="all, delete-orphan")

    def to_dict(self):
        board_dict = dict(
            id=self.id,
            title=self.title,
            owner=self.owner,
        )

        return board_dict

    @classmethod
    def from_dict(cls, board_data):
        return cls(
            title=board_data["title"],
            owner=board_data["owner"],
        )