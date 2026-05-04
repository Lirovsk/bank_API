import uuid
from uuid import UUID

from .. import db
from . import id_uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Numeric, Date, ForeignKey
from typing import List, Optional
from decimal import Decimal

from datetime import date



class User(db.Model):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    accounts: Mapped[List["Account"]] = relationship(
        "Account", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User: {self.name} ({self.email})>"


class Account(db.Model):
    __tablename__ = "accounts"

    id: Mapped[id_uuid]
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    last_transaction_date: Mapped[date] = mapped_column(
        Date, nullable=False, default=date.today
    )
    transaction_counter: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="accounts")

    def __repr__(self):
        return f"<Account: {self.type} with balance {self.balance} for user {self.user.name}>"
