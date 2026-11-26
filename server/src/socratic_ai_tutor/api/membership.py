from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from socratic_ai_tutor.core.security import get_current_user
from socratic_ai_tutor.core.database import get_db
from socratic_ai_tutor.models import User
from socratic_ai_tutor.repository.order import OrderRepository
from socratic_ai_tutor.repository.user import UserRepository
from socratic_ai_tutor.schema.membership import CreateOrderRequest
from socratic_ai_tutor.services import membership

router = APIRouter(prefix="/membership", tags=["Membership"])


@router.get('/plans')
def get_plans():
    return membership.list_membership_plans()


@router.post('/orders')
async def create_membership_order(
    req: CreateOrderRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return {'id': await membership.create_membership_order(user, req.plan, db)}


@router.get('/orders')
async def get_membership_orders(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return {'orders': await membership.get_membership_orders(user, db)}


@router.get('/orders/{id}')
async def get_order(
    id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return await membership.get_order(id, db, user)


@router.post('/activate')
async def activate_membership(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await OrderRepository.get_order_by_id(
        db, order_id, for_update=True
    )

    if order is None:
        raise HTTPException(404, '订单不存在')

    if order.status != 'paid':
        raise HTTPException(400, '订单状态不正确')

    user = await UserRepository.get_user_by_id(
        db, order.user_id, for_update=True
    )

    if user is None:
        raise HTTPException(404, '用户不存在')

    await membership.activate_membership(user, order)

    await db.commit()
