import uuid

from .. import db
from . import id_uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Numeric, Date, ForeignKey
from typing import List, Optional
from decimal import Decimal

from datetime import date


class Account(db.Model):
    __bind_key__ = "accounts"
    __tablename__ = "accounts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_uuid: Mapped[str] = mapped_column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    account_type: Mapped[str] = mapped_column(String(50), nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[Date] = mapped_column(Date, nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False)
    last_transaction_date: Mapped[Date] = mapped_column(Date, nullable=False, default=date.today)
    
