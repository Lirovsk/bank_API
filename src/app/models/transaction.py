from app import db
from .account import Account

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Numeric, DateTime, ForeignKey
from typing import List, Optional

from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    amount: Mapped[Numeric] = mapped_column(nullable=False)
    date: Mapped[DateTime] = mapped_column(nullable=False, default=datetime.now(tz=None))
    account_maker_id: Mapped[str] = mapped_column(String(50), nullable=False)
    account_receiver_id: Mapped[str] = mapped_column(String(50), nullable=True)
    