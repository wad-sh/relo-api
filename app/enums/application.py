from enum import Enum

class ApplicationStatus (str,Enum) :
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class VehicleType (str,Enum):
    BICYCLE = "bicycle"
    MOTORCYCLE = "motorcycle"
    CAR = "car"
    SUV = "suv"
    VAN = "van"
    PICKUP_TRUCK = "pickup_truck"
    TRUCK = "truck"
    BUS = "bus"
    OTHER = "other"

