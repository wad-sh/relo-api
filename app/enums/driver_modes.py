from enum import Enum

class DrivingMode (str, Enum):
    OFF = "off"
    LOCAL = "local"
    FLEXIBLE = "flexible"
    TRIP = "trip"