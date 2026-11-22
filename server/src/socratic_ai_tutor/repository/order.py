from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from socratic_ai_tutor.models import Order


class OrderRepository:
    @staticmethod
    async def create_order(db: AsyncSession, plan: dict, user_id: int):
        order = Order(
            user_id=user_id,
            plan_code=plan['code'],
            amount=plan['price'],
            duration_days=plan['duration_days'],
            status="pending",
        )
        db.add(order)
        await db.flush()
        await db.commit()
        return order.id

    @staticmethod
    async def get_order_by_id(db: AsyncSession, id: int, user_id: int | None = None, for_update: bool = False):
        stmt = select(Order).where(Order.id == id)

        if user_id is not None:
            stmt = stmt.where(Order.user_id == user_id)

        if for_update:
            stmt = stmt.with_for_update()

        return await db.scalar(stmt)
