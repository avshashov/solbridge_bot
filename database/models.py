from datetime import datetime, timedelta
from sqlalchemy import BigInteger, String, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


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
    created_at: Mapped[datetime] = mapped_column(default=datetime.now() + timedelta(hours=9))
    open: Mapped[bool] = mapped_column(default=True)
    paid: Mapped[bool] = mapped_column(default=False)
    canceled: Mapped[bool] = mapped_column(default=False)
    url: Mapped[str] = mapped_column(nullable=True)


class PreOrders(Base):
    __tablename__ = 'pre_orders'

    order_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    product: Mapped[str] = mapped_column(String(5), nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)


class PostQueue(Base):
    __tablename__ = 'post_queue'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[bool]
    user_id: Mapped[int] = mapped_column(BigInteger)
    type: Mapped[str] = mapped_column(String(8), nullable=False)
    text: Mapped[str] = mapped_column(Text)
    file_id: Mapped[str] = mapped_column(Text)
    target: Mapped[bool]
