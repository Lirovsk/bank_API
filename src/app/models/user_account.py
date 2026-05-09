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

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    
    accounts: Mapped[List["Account"]] = relationship("Account", back_populates="user")

    def __repr__(self):
        return f"<User: {self.name} ({self.email})>"


class Account(db.Model):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_type: Mapped[str] = mapped_column(String(50), nullable=False)
    account_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="accounts")
    
    def __repr__(self):
        return f"<Account: id: {self.id}, account_type: {self.account_type}, account_number: {self.account_number}"
