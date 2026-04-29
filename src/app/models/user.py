import uuid

from app import db
from .account import Account

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import List, Optional


class User(db.Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    accounts: Mapped[List['Account']] = relationship('Account', back_populates='user', cascade='all, delete-orphan')
    

    def __repr__(self):
        return f'<User: {self.name} ({self.email})>'