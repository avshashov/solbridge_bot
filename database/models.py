from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


def create_tables(engine):
    Base.metadata.create_all(engine)


class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]
    username: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str]
    instagram: Mapped[str]


class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[str] = mapped_column(unique=True)
    product: Mapped[str] = mapped_column(String(5), nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    # updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now)
    open: Mapped[bool] = mapped_column(default=True)
    paid: Mapped[bool] = mapped_column(default=False)
    canceled: Mapped[bool] = mapped_column(default=False)
    url: Mapped[str] = mapped_column(nullable=True)
