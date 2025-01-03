from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    like_count: Mapped[int]
    boards: Mapped[list["Board"]] = relationship(back_populates="card")

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
