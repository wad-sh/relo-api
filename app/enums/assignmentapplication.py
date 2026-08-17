from enum import Enum

class AssignmenApplicationtStatus (str, Enum):
    PENDING = "pending"
    ACCEPTED ="accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    ERROR ="error"