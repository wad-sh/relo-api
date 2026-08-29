from app.models.driver import Driver
from app.schemas.order_schemas import OrderUpdateStatus,OrderCreate,OrderUpdate
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User
from fastapi import HTTPException
from app.models.trip import Trip
from app.models.order import Order
from app.enums.order import OrderStatus
from app.services.user_service import exist_user
from app.services.driver_service import valid_driver
from app.enums.driver_modes import DrivingMode as Mode
from app.enums.order import OrderStatus,OrderType
from app.services.history_service import create_history
from app.services.assignment_service import create_assignment,cancel_assignment

def create_order (db : Session, user: User,data: OrderCreate):
    exist_user(db,user.id)
    valid_area_route(data)

    new_order = Order(
    type = data.type,
    operating_area = data.operating_area,
    route_from= data.route_from,
    route_to=data.route_to,
    address_receive=data.address_receive,
    address_delivery=data.address_delivery,
    description=data.description,
    )

    db.add(new_order)
    db.flush()
    create_assignment(db,new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

def update_order (db : Session,order_id: int, user: User,data: OrderUpdate):
    exist_user(db,user.id)
    order = exist_order(db,order_id)
    ur_order_customer(db,user,order_id)
    valid_order_edit(db,order_id)

    if data.type is None and data.operating_area is None and data.route_from is None and data.route_to is None and data.address_receive is None and data.address_delivery is None and data.description is None :
        raise HTTPException(
            status_code=400,
            detail="no change"
        )
    

    final_type= data.type if data.type is not None else order.type
    final_area= data.operating_area if data.operating_area is not None else order.operating_area
    final_to = data.route_to if data.route_to is not None else order.route_to
    final_from = data.route_from if data.route_from is not None else order.route_from

    if final_type == OrderType.LOCAL:
        if final_area is None:
            raise HTTPException(
                status_code=400,
                detail="for local orders u need to add the area not the route"
            )
        final_from = None
        final_to= None

    if final_type == OrderType.ROUTE:
        if final_to is None:
            raise HTTPException(
                status_code=400,
                detail="for route orders u need to add a full route not area"
            )
        if final_from is None:
            raise HTTPException(
                status_code=400,
                detail="for route orders u need to add a full route not area"
            )
        if final_to == final_from:
            raise HTTPException(
                status_code=400,
                detail="invalid route"
            )
        final_area = None


    order.type = final_type
    order.operating_area = final_area
    order.route_from = final_from
    order.route_to = final_to


    if data.address_receive is not None:
        order.address_receive=data.address_receive
    if data.address_delivery is not None:
        order.address_delivery=data.address_delivery
    if data.description is not None:
        order.description=data.description
    
    cancel_assignment(db,order)
    create_assignment(db,order)
    db.commit()
    db.refresh(order)
    return order

def update_status_admin_order (db: Session, order_id : int, data: OrderUpdateStatus,more_details:str,admin: User) :
    order = exist_order(db,order_id)
    
    old_status = order.status
    if old_status == data.status:
        raise HTTPException(
        status_code=409,
        detail="no change"
    )
    order.status = data.status
    
    history = create_history(order_id,old_status,order.status,admin.id,more_details)

    db.add(history)
    if order.status != OrderStatus.PENDING:
        cancel_assignment(db, order)
    db.commit()
    db.refresh(order)
    db.refresh(history)
    return order

def update_status_order (db: Session, order_id : int,user:User):
        valid_driver(db,user)
        order = exist_order(db,order_id)
        ur_order_driver(db,user,order_id)
        old_status = order.status
        if order.status == OrderStatus.ACCEPTED:
            order.status = OrderStatus.IN_TRANSIT
        elif order.status == OrderStatus.IN_TRANSIT:
            order.status = OrderStatus.DELIVERED
        else:
            raise HTTPException(
                status_code=409,
                detail="order already delivered"
            )
        history = create_history(order_id,old_status,order.status,user.id)
        db.add(history)
        db.commit()
        db.refresh(order)
        db.refresh(history)
        return order


def get_my_orders_customer (db: Session, user:User) :
    exist_user(db,user.id)
    return db.query(Order).filter(Order.order_owner_id == user.id).all()

def get_my_orders_driver (db:Session, user:User) :
    valid_driver(db,user)
    return db.query(Order).filter(Order.driver_id == user.id).all()

def cancel_order (db:Session, user:User,order_id: int) :
    exist_user(db,user.id)
    order = exist_order(db,order_id)
    ur_order_customer(db,user,order_id)
    valid_order_edit(db,order_id)
    order.status = OrderStatus.CANCELLED
    cancel_assignment(db, order)

    db.commit()
    db.refresh(order)
    return {
        "message" : "your order has been cancelled"
    }

def make_order_avilable(db:Session,user:User,order_id:int) :
    valid_driver(db,user)
    order = exist_order(db,order_id)
    ur_order_driver(db,user,order_id)
    valid_order_cancel_driver(db,order_id)
    cancel_assignment(db, order)

    order.status = OrderStatus.PENDING
    order.driver_id = None

    create_assignment(db, order)

    db.commit()
    return order



def valid_area_route (data) :
    if (data.type == OrderType.LOCAL) and (data.operating_area is None):
        raise HTTPException(
            status_code=400,
            detail="add operating area for local orders"
        )
    if (data.type == OrderType.ROUTE) and (data.route_from is None or data.route_to is None):
        raise HTTPException(
            status_code=400,
            detail="add full route for the order"
        )

    if(data.type == OrderType.ROUTE) and (data.route_to == data.route_from) :
            raise HTTPException(
             status_code=400,
             detail="invalid route"
        )

def exist_order (db: Session, order_id: int) :
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None :
        raise HTTPException (
             status_code=404,
             detail="order not found"
        )
    return order

def ur_order_customer (db: Session,user:User,order_id:int) :
    order = db.query(Order).filter(Order.id == order_id,Order.order_owner_id == user.id).first()
    if order is None :
        raise HTTPException (
             status_code=404,
             detail="order not found"
        )

def ur_order_driver (db: Session,user:User,order_id:int) :
    order = db.query(Order).filter(Order.id == order_id,Order.driver_id == user.id).first()
    if order is None :
        raise HTTPException (
             status_code=404,
             detail="order not found"
        )

def valid_order_edit (db:Session,order_id:int):
    order=db.query(Order).filter(Order.id == order_id).first()
    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=409,
            detail="order is not avilable for edit"
        )

def valid_order_cancel_driver (db:Session,order_id:int):
    order=db.query(Order).filter(Order.id == order_id).first()
    if order.status != OrderStatus.ACCEPTED:
        raise HTTPException(
            status_code=409,
            detail="can't make the order avilable again"
        )