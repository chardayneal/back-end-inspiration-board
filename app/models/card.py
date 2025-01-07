from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import ForeignKey

class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    like_count: Mapped[int]
    board_id: Mapped[int] = mapped_column(ForeignKey("board.id"))
    board: Mapped["Board"] = relationship("Board", back_populates="cards")

    def to_dict(self):
        card_dict = dict(
            id=self.id,
            message=self.message,
            like_count=self.like_count,
        )

        return card_dict
    
    @classmethod
    def from_dict(cls, card_data):
        return cls(
            message=card_data["message"],
            like_count=card_data["like_count"],
        )
