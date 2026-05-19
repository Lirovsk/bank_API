from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import ForeignKey, DateTime, Integer, func
from typing import List

from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    balance: Mapped[int] = mapped_column(nullable=False)
    is_banker: Mapped[bool] = mapped_column(default=False)
    
    sender_transactions: Mapped[List["Transaction"]] = relationship("Transaction",
                                                                    foreign_keys="[Transaction.sender_id]",
                                                                    back_populates="sender")
    recipient_transactions: Mapped[List["Transaction"]] = relationship("Transaction",
                                                                    foreign_keys="[Transaction.recipient_id]",
                                                                    back_populates="recipient")

    def __repr__(self):
        return f"Player(id={self.id}, name='{self.name}', balance={self.balance}, is_banker={self.is_banker})"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"), nullable=False)
    recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"), nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
    sender: Mapped["Player"] = relationship("Player", 
                                            foreign_keys=[sender_id], 
                                            back_populates="sender_transactions")
    recipient: Mapped["Player"] = relationship("Player", 
                                               foreign_keys=[recipient_id], 
                                               back_populates="recipient_transactions")
