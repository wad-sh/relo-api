from app.models.driver import Driver
from app.schemas.driver_schemas import DriverMode,OperatingArea
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User
from fastapi import HTTPException
from app.models.trip import Trip
from app.enums.trip import TripStatus
from app.models.order import Order
from app.enums.order import OrderStatus
from app.services.user_service import exist_user
from app.enums.driver_modes import DrivingMode as Mode






def update_mode_driver (db: Session,user: User ,data : DriverMode  ):
    valid_update(db,user)

    if data.mode == user.driver.mode :
          raise HTTPException(
                status_code= 409,
                detail= "no change"
          )

    user.driver.mode = data.mode
    if data.mode not in [Mode.LOCAL, Mode.FLEXIBLE]:
        user.driver.area = None
    db.commit()
    db.refresh(user)

    return{
        "message" : "mode updated successfully. don't forget to change the operatring area if your mode is local or flexible"
    }


def update_area_driver (db: Session,user: User ,data : OperatingArea) : 
    valid_area_update(db,user)
    if data.area == user.driver.area :
          raise HTTPException(
                status_code= 409,
                detail= "no change"
          )

    user.driver.area = data.area
    db.commit()
    db.refresh(user)
    return user.driver
          

def valid_update (db: Session, user:User) :
    exist_user(db,user.id)

    has_trips = db.query(Trip).filter(Trip.driver_id == user.id, or_( 
        Trip.status == TripStatus.PLANNED , Trip.status == TripStatus.ACTIVE
    )).first()

    if has_trips is not None :
            raise HTTPException(
                status_code= 409,
                detail="you have trips planned or active"
            )

    
    has_orders = db.query(Order).filter(
    Order.driver_id == user.id,
    Order.status.in_([OrderStatus.ACCEPTED, OrderStatus.IN_TRANSIT])).first()

    if has_orders is not None :
            raise HTTPException(
                status_code= 409,
                detail="you have active orders as a driver"
            )

def valid_area_update (db: Session,user: User) :
    valid_update(db,user)
    if user.driver.mode not in [Mode.LOCAL,Mode.FLEXIBLE] :
        raise HTTPException(
             status_code=400,
             detail="mode should be local or flexible to change area"
        )