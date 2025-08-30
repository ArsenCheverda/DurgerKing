from sqlalchemy import select
from models import async_session, User, Order, OrderItem
from typing import List

# This is a temporary import, as OrderItem for API is defined in main.py
from main import OrderItem as OrderItemSchema


async def add_user(tg_id: int, first_name: str):
    """Finds a user by tg_id or creates a new one."""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user

        new_user = User(tg_id=tg_id, first_name=first_name)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def add_order(user_id: int, items: List[OrderItemSchema], total_price: float, comment: str = None):
    """Creates a new order and its associated items in the database."""
    async with async_session() as session:
        # Create the main order record
        new_order = Order(
            user_id=user_id,
            total_price=total_price,
            comment=comment
        )
        session.add(new_order)
        await session.flush()  # Flush to get the new_order.id before committing

        # Create the individual item records
        for item in items:
            new_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            session.add(new_item)

        await session.commit()
