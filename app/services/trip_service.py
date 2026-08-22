from app.models.driver import Driver
from app.schemas.trip_schemas import TripStatus,TripCreate,TripUpdateroute,TripUpdateStatus
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User
from fastapi import HTTPException
from app.models.trip import Trip
from app.models.order import Order
from app.enums.order import OrderStatus
from app.services.driver_service import valid_driver
from app.enums.driver_modes import DrivingMode as Mode


def create_trip (db: Session,user:User,data: TripCreate) :
    valid_driver(db,user)
    valid_mode(user)
    no_trips_driver(db,user)
    no_orders_driver(db,user)

    if data.route_to == data.route_from :
        raise HTTPException(
             status_code=400,
             detail="invalid route"
        )

    new_trip = Trip(
        driver_id = user.id,
        route_from = data.route_from,
        route_to = data.route_to
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip

def get_planned_trips_by_route (db: Session, data: TripUpdateroute) :
     return db.query(Trip).filter(Trip.status == "planned", Trip.route_from == data.route_from, Trip.route_to == data.route_to).all()

def update_route_trip (db: Session,user:User,trip_id: int ,data: TripUpdateroute) : 
    valid_driver(db,user)
    valid_mode(user)
    trip = existed_trip_for_driver(db,user,trip_id)
    if data.route_to == data.route_from :
        raise HTTPException(
             status_code=400,
             detail="invalid route"
        )
    if    trip.route_to == data.route_to and trip.route_from == data.route_from:
        raise HTTPException(
            status_code=409,
            detail="no change"
        )
    trip.route_to = data.route_to
    trip.route_from = data.route_from

    db.commit()
    db.refresh(trip)
    return trip
    
    
      

def update_status_trip (db: Session,user:User,trip_id: int) : 
    valid_driver(db,user)
    valid_mode(user)
    trip = existed_trip_for_driver(db,user,trip_id)

    if trip.status == TripStatus.PLANNED:
        trip.status = TripStatus.ACTIVE
    elif trip.status == TripStatus.ACTIVE:
        trip.status = TripStatus.COMPLETED
    else :
        raise HTTPException(
            status_code=409,
            detail="only liner change for trips status"
        )
    db.commit()
    db.refresh(trip)
    return trip



def update_status_admin_trip (db: Session,trip_id: int,data: TripUpdateStatus) : 
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if trip is None :
        raise HTTPException(
            status_code=404,
            detail="trip not found"
        )
    trip.status = data.status
    db.commit()
    db.refresh(trip)
    return trip



def delete_trip (db: Session,user:User,trip_id: int) : 
    valid_driver(db,user)
    trip = existed_trip_for_driver(db,user,trip_id)
    orders = db.query(Order).filter(
    Order.trip_id == trip_id,
    Order.status.in_([
        OrderStatus.ACCEPTED,
        OrderStatus.IN_TRANSIT
    ])
    ).first()
    if orders is not None :
        raise HTTPException(
            status_code=409,
            detail="there is orders related to this trip make them avilable first"
        )
    db.delete(trip)
    db.commit()
    return {
        "message" : "trip got deleted successfully"
    }




def valid_mode (user:User) :
    if user.driver.mode not in [Mode.TRIP,Mode.FLEXIBLE] :
            raise HTTPException(
                 status_code=400,
                 detail="mode should be trip or flexible to change area"
            )

def no_trips_driver (db: Session,user:User) :
    act_trips = db.query(Trip).filter(Trip.driver_id == user.id, Trip.status.in_ ([TripStatus.PLANNED,TripStatus.ACTIVE]) ).first()
    if act_trips is not None :
        raise HTTPException(
            status_code=409,
            detail="you have planned or active trips"
        )

def no_orders_driver (db: Session,user:User) :
    act_orders = db.query(Order).filter(Order.driver_id == user.id, Order.status.in_ ([OrderStatus.ACCEPTED,OrderStatus.IN_TRANSIT]) ).first()
    if act_orders is not None :
        raise HTTPException(
            status_code=409,
            detail="you have accepted or in transit orders"
        )

def existed_trip_for_driver (db: Session,user: User,trip_id:int) :
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.driver_id == user.id).first()
    if trip is None :
        raise HTTPException(
            status_code=404,
            detail="unable to find trip"
        )
    return trip