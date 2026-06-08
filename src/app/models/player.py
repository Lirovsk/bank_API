from ...app import db

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Boolean
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game
    from .transaction import Transaction


class Player(db.Model):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    balance: Mapped[int] = mapped_column(Integer, nullable=False)
    is_banker: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    game: Mapped["Game"] = relationship("Game", back_populates="players")
    game_uuid: Mapped[str] = mapped_column(
        String(36), ForeignKey("games.id"), nullable=False
    )
    transactions_made: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        foreign_keys="Transaction.sender_id",
        back_populates="sender",
    )
    transactions_received: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        foreign_keys="Transaction.recipient_id",
        back_populates="recipient",
    )

    def __repr__(self):
        return (
            f"<Player(id={self.id}, name='{self.name}', game_uuid='{self.game_uuid}')>"
        )


from .transaction import Transaction
