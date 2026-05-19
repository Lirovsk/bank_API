from ..app import db

import uuid

from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

class Game(db.Model):
    __tablename__ = "games"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    bonus_per_round: Mapped[int] = mapped_column(Integer, nullable=False)
    rules_from: Mapped[str] = mapped_column(String, nullable=True)
    
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=db.func.now())
    transactions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    last_modified: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    
    def __repr__(self):
        return f"Game(id='{self.id}', bonus_per_round={self.bonus_per_round}, rules_from='{self.rules_from}', created_at='{self.created_at}', transactions_count={self.transactions_count}, last_modified='{self.last_modified}')"
