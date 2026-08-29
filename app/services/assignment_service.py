from app.models.driver import Driver
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User
from fastapi import HTTPException
from app.models.trip import Trip
from app.models.order import Order
from app.models.driver_assignment import DriverAssignment
from app.enums.order import OrderStatus
from app.services.user_service import exist_user
from app.services.driver_service import valid_driver
from app.enums.driver_modes import DrivingMode as Mode
from app.enums.order import OrderStatus,OrderType
from app.services.history_service import create_history
from app.enums.assignment import AssignmentStatus
from datetime import datetime,timezone
from app.enums.trip import TripStatus

def create_assignment (db:Session,order:Order) :
    if order.type == OrderType.LOCAL:
        drivers = db.query(Driver).filter(Driver.mode==Mode.LOCAL,Driver.local_operating_area == order.operating_area).all()
      
    elif order.type == OrderType.ROUTE:
        drivers = db.query(Driver).join(Trip).filter(
            Driver.mode==Mode.TRIP,
            Trip.route_from == order.route_from,
            Trip.route_to==order.route_to,
            Trip.status == TripStatus.PLANNED
            ).all()

    for driver in drivers :
        new_assignment = DriverAssignment(
                order_id = order.id,
                driver_id = driver.id
            )
        db.add(new_assignment)


def cancel_assignment (db:Session,order: Order):
    assignments = db.query(DriverAssignment).filter(DriverAssignment.order_id == order.id).all()
    for a in assignments :
        a.status = AssignmentStatus.EXPIRED





def get_assignmnet_driver (db:Session,user:User) :
    valid_driver(db,user)
    return db.query(DriverAssignment).filter(DriverAssignment.driver_id == user.id).all()

def accept_assignment_driver (db:Session,user:User,assignment_id:int) :
    try :
        valid_driver(db,user)
        assignmnet = db.query(DriverAssignment).filter(
            DriverAssignment.id == assignment_id,
            DriverAssignment.driver_id == user.id,
            DriverAssignment.status == AssignmentStatus.PENDING
        ).first()
        if assignmnet is None :
            raise HTTPException(
                status_code=404,
                detail="assignment not found"
            )
        order = db.query(Order).with_for_update().filter(Order.id == assignmnet.order_id).first()
        driver = db.query(Driver).with_for_update().filter(Driver.id == user.id).first()

        if order is None or order.status != OrderStatus.PENDING:
            raise HTTPException(
                status_code=404,
                detail="order not found"
            )

        count = db.query(Order).filter(
            Order.driver_id == driver.id,
            Order.status.in_([
                OrderStatus.ACCEPTED,
                OrderStatus.IN_TRANSIT
            ])
        ).count()

        if count >= 5:
            raise HTTPException(
                status_code=409,
                detail="you can not have more than 5 active orders at the same time"
            )
        other_assignmnts = db.query(DriverAssignment).filter(DriverAssignment.order_id == order.id).all()
        if other_assignmnts :
            for a in other_assignmnts :
                a.status = AssignmentStatus.EXPIRED
        assignmnet.status = AssignmentStatus.TAKEN
        assignmnet.responded_at = datetime.now(timezone.utc)
        order.status = OrderStatus.ACCEPTED
        order.driver_id =driver.id
        db.commit()
        db.refresh(assignmnet)
        db.refresh(order)
    except HTTPException :
        db.rollback()
        raise
    except Exception :
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
    return assignmnet
    
