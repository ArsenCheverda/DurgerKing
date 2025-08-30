from sqlalchemy import ForeignKey, String, BigInteger, Float, Integer
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from typing import List

# Database connection engine
engine = create_async_engine(url='sqlite+aiosqlite:///durger_king.sqlite3', echo=True)

# Async session factory
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(128), nullable=True)
    
    orders: Mapped[List["Order"]] = relationship(back_populates="user")


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    total_price: Mapped[float] = mapped_column(Float)
    comment: Mapped[str] = mapped_column(String(500), nullable=True)
    
    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(Integer) # Corresponds to product ID on frontend
    quantity: Mapped[int] = mapped_column(Integer)

    order: Mapped["Order"] = relationship(back_populates="items")


async def init_db():
    """Creates all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
