from datetime import datetime, timedelta, timezone
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from socratic_ai_tutor.models import Order, User
from socratic_ai_tutor.repository.order import OrderRepository


MEMBERSHIP_PLANS = [
    {
        'code': 'free',
        'name': 'Free',
        'price': 0,
        'duration_days': None,
        "conversation_limit": 3,
        "conversation_limit_type": "lifetime",
        "conversation_token_limit": 8000,
        'describe': [
            '仅 3 次对话',
            '单对话长度有限'
        ]
    },
    {
        'code': 'plus',
        'name': 'Plus',
        'price': 2400,
        'duration_days': 30,
        "conversation_limit": 10,
        "conversation_limit_type": "daily",
        "conversation_token_limit": 10000,
        'describe': [
            '每日 10 次对话',
            '解锁错题功能',
            '单对话长度 8000 Token'
        ]
    },
    {
        'code': 'pro',
        'name': 'Pro',
        'price': 4800,
        'duration_days': 30,
        "conversation_limit": 20,
        "conversation_limit_type": "daily",
        "conversation_token_limit": 50000,
        'describe': [
            '每日 20 次对话',
            '解锁错题功能',
            '单对话长度 10000 Token',
            '升级时，当前会员剩余时间将按照原套餐与新套餐的价格比例折算，并计入新会员有效期。'
        ]
    },
]


async def create_membership_order(user: User, plan_code: str, db: AsyncSession):
    plan = next(
        (p for p in MEMBERSHIP_PLANS if p["code"] == plan_code),
        None
    )

    if plan is None:
        raise HTTPException(status_code=404, detail='套餐不存在')

    return await OrderRepository.create_order(db, plan, user.id)


async def get_membership_orders(user: User, db: AsyncSession):
    orders = await db.scalars(
        select(Order)
        .where(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
    )

    return orders.all()


async def get_order(id: int, db: AsyncSession, user: User):
    order = await OrderRepository.get_order_by_id(db, id, user.id)
    if order is None:
        raise HTTPException(status_code=404, detail='订单不存在')

    return order


def convert_membership_time(
    remaining: timedelta,
    old_price: int,
    old_duration: int,
    new_price: int,
    new_duration: int
) -> timedelta:

    old_daily_price = Decimal(old_price) / old_duration
    new_daily_price = Decimal(new_price) / new_duration

    ratio = old_daily_price / new_daily_price

    return remaining * float(ratio)


async def activate_membership(user: User, order: Order):
    now = datetime.now(timezone.utc)
    plan = next(
        (p for p in MEMBERSHIP_PLANS if p["code"] ==
         order.plan_code and p['code'] != 'free'),
        None
    )

    if plan is None:
        raise HTTPException(status_code=404, detail='套餐不存在')

    if user.membership_expire_at is None or user.membership_expire_at < now:
        user.membership_expire_at = now + timedelta(days=plan['duration_days'])
    else:

        if user.membership_plan == 'pro' and plan['code'] == 'plus':
            raise HTTPException(400, '不允许降级会员')

        old_plan = next(
            (p for p in MEMBERSHIP_PLANS if p["code"] == user.membership_plan),
            None
        )

        if old_plan is None:
            raise HTTPException(500, '当前会员套餐配置异常')

        remaining = user.membership_expire_at - now
        user.membership_expire_at = (
            now
            + timedelta(days=plan['duration_days'])
            + convert_membership_time(
                remaining,
                old_plan['price'],
                old_plan['duration_days'],
                plan['price'],
                plan['duration_days']
            )
        )

    user.membership_plan = plan['code']
    order.status = 'completed'
