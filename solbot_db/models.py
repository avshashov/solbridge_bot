import sqlalchemy as sq
from sqlalchemy.orm import DeclarativeBase, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


def create_tables(engine):
    Base.metadata.create_all(engine)


class Users(Base):
    __tablename__ = 'users'

    user_id = mapped_column(sq.BigInteger, primary_key=True)
    name = mapped_column(sq.String(30))
    username = mapped_column(sq.String(30), default=None)
    email = mapped_column(sq.String(30))
    instagram = mapped_column(sq.String(30))


class Orders(Base):
    __tablename__ = 'orders'

    id = mapped_column(sq.Integer, primary_key=True)
    order_id = mapped_column(sq.Text, unique=True)
    user_id = mapped_column(sq.BigInteger, sq.ForeignKey('users.user_id'), nullable=False)
    created_at = mapped_column(sq.DateTime, default=datetime.now())
    open = mapped_column(sq.Boolean, default=True)
    paid = mapped_column(sq.Boolean, default=False)
    canceled = mapped_column(sq.Boolean, default=False)
    url = mapped_column(sq.Text)


class Blacklist(Base):
    __tablename__ = 'blacklist'

    user_id = mapped_column(sq.BigInteger, primary_key=True)
    username = mapped_column(sq.String(30), default=None)
    created_at = mapped_column(sq.DateTime, default=datetime.now())


class Admins(Base):
    __tablename__ = 'admins'

    user_id = mapped_column(sq.BigInteger, primary_key=True)
