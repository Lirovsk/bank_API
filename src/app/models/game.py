from ...app import db

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime
from uuid import uuid4
from typing import List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .player import Player

class Game(db.Model):
    __tablename__ = "games"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    game_used: Mapped[str] = mapped_column(String(50), nullable=False)
    bonus_per_round: Mapped[int] = mapped_column(Integer, nullable=False)
    start_value: Mapped[int] = mapped_column(Integer, nullable=False, default=1000)
    time_of_last_transaction: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(tz=None), onupdate=lambda: datetime.now(tz=None))
    number_of_operations: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    players: Mapped[List["Player"]] = relationship("Player", back_populates="game")
    
    def __repr__(self):
        return f"<Game(id='{self.id}', time_of_last_transaction='{self.time_of_last_transaction}', number_of_operations={self.number_of_operations})>"
