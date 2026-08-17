from enum import Enum

class TripStatus (str, Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"

    EXPIRED = "expired"
    ERORR ="error"