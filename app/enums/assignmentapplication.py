from enum import Enum

class AssignmenApplicationtStatus (str, Enum):
    WAITING = "waiting"
    TAKEN = "taken"
    EXPIRED = "expired"