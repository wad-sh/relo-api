from app.models.driver import Driver
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User
from fastapi import HTTPException
from app.models.trip import Trip
from app.models.order import Order
from app.enums.order import OrderStatus
from app.services.user_service import exist_user
from app.enums.order import OrderStatus,OrderType
from app.models.history_order import HistoryOrder


def create_history (o_id: int,old_s: OrderStatus,new_s:OrderStatus,u_id:int,det: str | None = None) :
    new_history = HistoryOrder(
        order_id = o_id,
        old_status = old_s,
        new_status = new_s,
        changed_by_id = u_id,
        more_details = det
    )
    return new_history


def get_by_order(db:Session,order_id:int) : 
    return db.query(HistoryOrder).filter(HistoryOrder.order_id==order_id).all()


