from pydantic import BaseModel,ConfigDict
from app.enums.trip import TripStatus
from app.enums.route_enum import Governorate
from datetime import datetime

class TripResponse (BaseModel) :
    id : int
    driver_id : int
    created_at : datetime
    route_from : Governorate
    route_to:Governorate
    status :TripStatus
    model_config = ConfigDict(from_attributes=True)

class TripCreate (BaseModel) :
    route_from : Governorate
    route_to: Governorate

class TripUpdateroute (BaseModel) :
    route_from : Governorate
    route_to: Governorate

class TripUpdateStatus (BaseModel) :
    status : TripStatus

class Tripsearsh (BaseModel) :
    route_from : Governorate
    route_to: Governorate
