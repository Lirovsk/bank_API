from ...app import db

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey
from typing import List, TYPE_CHECKING
from datetime import datetime


if TYPE_CHECKING:
    from .player import Player
    from .game import Game


class Transaction(db.Model):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_type: Mapped[str] = mapped_column(String(12), nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    game_uuid: Mapped[str] = mapped_column(String(36), ForeignKey("games.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(tz=None)
    )

    sender_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    recipient_id: Mapped[int] = mapped_column(ForeignKey("players.id"))

    sender: Mapped["Player"] = relationship("Player",
                                            foreign_keys=[sender_id],
                                            back_populates="transactions_made")
    recipient: Mapped["Player"] = relationship("Player",
                                                foreign_keys=[recipient_id],
                                                back_populates="transactions_received")

    def __repr__(self):
        return f"<Transaction(id={self.id}, type='{self.transaction_type}', value={self.value}, game_uuid='{self.game_uuid}')>"