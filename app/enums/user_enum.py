from enum import Enum

class UserEnum (str, Enum):
    Customer = "Customer"
    Admin = "Admin"
    Driver = "Driver"