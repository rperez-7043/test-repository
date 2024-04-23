from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy import func
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Joke(Base):
    __tablename__ = "jokes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    setup: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    punchline: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    published: Mapped[bool] = mapped_column(
        nullable=False,
        server_default='1'
    )
    create_date: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now()
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    email: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    password: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
