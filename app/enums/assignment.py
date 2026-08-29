from enum import Enum

class AssignmentStatus (str, Enum):
    WAITING = "waiting"
    TAKEN = "taken"
    EXPIRED = "expired"