from enum import Enum

class OrderStatus (str, Enum):
    PENDING = "pending"
    ACCEPTED ="accepted"
    IN_TRANSIT = "in_transit"
    DELIVERED ="delivered"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    ERROR ="error"

class OrderType (str, Enum):
    LOCAL = "local"
    ROUTE ="route"