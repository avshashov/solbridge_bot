from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PreOrders(Base):
    __tablename__ = 'pre_orders'

    order_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    product: Mapped[str] = mapped_column(String(5), nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
