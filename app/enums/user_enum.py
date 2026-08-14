from enum import Enum

class UserEnum (Enum,str) :
    Customer = "Customer"
    Admin = "Admin"
    Driver = "Driver"