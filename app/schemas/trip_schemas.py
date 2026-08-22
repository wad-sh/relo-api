from pydantic import BaseModel,Field,ConfigDict
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

class TripCreate (BaseModel) :
    route_from : Governorate
    route_to: Governorate

class TripUpdateroute (BaseModel) :
    route_from : Governorate
    route_to: Governorate

class TripUpdateStatus (BaseModel) :
    status : TripStatus

