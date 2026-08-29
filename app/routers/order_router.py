from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.auth.dep import get_current_user,requires_admin
from app.schemas.order_schemas import (
    OrderCreate,
    OrderUpdate,
    OrderUpdateStatus,
    OrderResponse
)
from app.database.database import get_db
from app.services.order_service import update_order,make_order_avilable,update_status_admin_order,update_status_order,cancel_order,create_order,get_my_orders_customer,get_my_orders_driver
from app.models.user import User
from typing import List

order_router = APIRouter(
    prefix="/orders",
    tags=["Order"]
)

@order_router.post("",response_model=OrderResponse)
def create (data:OrderCreate,user:User =Depends(get_current_user)  ,db:Session=Depends(get_db)):
    return create_order(db,user,data)

@order_router.put("/{order_id}",response_model=OrderResponse)
def update (data:OrderUpdate,order_id:int,user:User =Depends(get_current_user)  ,db:Session=Depends(get_db)):
    return update_order(db,order_id,user,data)

@order_router.put("/{order_id}/status",response_model=OrderResponse)
def update_status (order_id:int,user:User =Depends(get_current_user)  ,db:Session=Depends(get_db)):
    return update_status_order(db,order_id,user)

@order_router.put("/{order_id}/status/admin",response_model=OrderResponse)
def update_status_admin (data:OrderUpdateStatus,order_id:int,more_details: str,admin:User = Depends(requires_admin),db:Session=Depends(get_db)):
    return update_status_admin_order(db,order_id,data,more_details,admin)

@order_router.put("/{order_id}/cancel",response_model=OrderResponse)
def cancel (order_id:int,user:User =Depends(get_current_user)  ,db:Session=Depends(get_db)):
    return cancel_order(db,user,order_id)

@order_router.get("/customer",response_model=List[OrderResponse])
def get_for_customer (user:User =Depends(get_current_user)  ,db:Session=Depends(get_db)):
    return get_my_orders_customer(db,user)

@order_router.get("/driver",response_model=List[OrderResponse])
def get_for_driver (user:User =Depends(get_current_user)  ,db:Session=Depends(get_db)):
    return get_my_orders_driver(db,user)

@order_router.put("/{order_id}/make-avilable",response_model=OrderResponse)
def make_avilable (order_id:int,user:User =Depends(get_current_user)  ,db:Session=Depends(get_db)):
    return make_order_avilable(db,user,order_id)