from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.auth.dep import get_current_user,requires_admin
from app.schemas.order_schemas import *
from app.database.database import get_db
from app.services.order_service import update_order,update_status_admin_order,update_status_order,cancel_order,create_order,get_my_orders_customer,get_my_orders_driver
from app.models.user import User
from typing import List

order_router = APIRouter(
    prefix="/orders",
    tags=["Order"]
)

@order_router.post("",response_model=OrderResponse)
def create (data:OrderCreate,user:User =Depends(get_current_user)  ,db:Session=Depends(get_db)):
    return create_order(db,user,data)

@order_router.put("",response_model=OrderResponse)
def update (data:Orderupdate,order_id:int,user:User =Depends(get_current_user)  ,db:Session=Depends(get_db)):
    return update_order(db,order_id,user,data)

@order_router.put("/status",response_model=OrderResponse)
def update_status (order_id:int,user:User =Depends(get_current_user)  ,db:Session=Depends(get_db)):
    return update_status_order(db,order_id,user)

@order_router.put("/status/admin",response_model=OrderResponse)
def update_status_admin (data:OrderUpdateStatus,order_id:int,db:Session=Depends(get_db)):
    return update_status_admin_order(db,order_id,data)

@order_router.put("/cancel",response_model=OrderResponse)
def cancel (order_id:int,user:User =Depends(get_current_user)  ,db:Session=Depends(get_db)):
    return cancel_order(db,user,order_id)

@order_router.get("/customer",response_model=List[OrderResponse])
def get_for_customer (user:User =Depends(get_current_user)  ,db:Session=Depends(get_db)):
    return get_my_orders_customer(db,user)

@order_router.get("/driver",response_model=List[OrderResponse])
def get_for_driver (user:User =Depends(get_current_user)  ,db:Session=Depends(get_db)):
    return get_my_orders_driver(db,user)