import uuid
from uuid import UUID

from app import db
from . import id_uuid
from .user import User

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Numeric, Date, ForeignKey
from typing import List, Optional

from datetime import date


class Account(db.Model):
    __tablename__ = 'accounts'
    
    id: Mapped[id_uuid]
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    balance: Mapped[Numeric] = mapped_column(nullable=False)
    last_transaction_date: Mapped[Date] = mapped_column(nullable=False, default=date.today())
    transaction_counter: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    user_id: Mapped[id_uuid] = mapped_column(ForeignKey('users.id'), nullable=False)
    
    user: Mapped[User] = relationship('User', back_populates='accounts')
    
    
    def __repr__(self):
        return f'<Account: {self.type} with balance {self.balance} for user {self.user.name}>'