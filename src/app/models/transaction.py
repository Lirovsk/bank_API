from .. import db

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Numeric, DateTime, ForeignKey
from typing import List, Optional
from decimal import Decimal

from datetime import datetime


class Transaction(db.Model):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    account_maker_id: Mapped[str] = mapped_column(String(50), nullable=False)
    account_receiver_id: Mapped[str] = mapped_column(String(50), nullable=True)
