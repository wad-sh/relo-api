from pydantic import BaseModel,ConfigDict,Field
from typing import Annotated,Union,Literal
from app.enums.order import OrderStatus,OrderType
from app.enums.route_enum import Governorate
from datetime import datetime

class OrderCreateLocal (BaseModel) :
    type : Literal[OrderType.LOCAL]
    operating_area :Governorate
    address_receive: str
    address_delivery:str
    description: str

class OrderCreateRoute (BaseModel) :
    type: Literal[OrderType.LOCAL]
    route_from: Governorate 
    route_to: Governorate 
    address_receive: str
    address_delivery:str
    description: str

OrderCreate = Annotated[
    Union[OrderCreateLocal,OrderCreateRoute],
    Field(discriminator=type)
]


class OrderResponse (BaseModel) : 
    id: int
    type: OrderType
    operating_area :Governorate | None = None
    route_from: Governorate | None = None
    route_to: Governorate | None = None
    address_receive: str
    address_delivery:str
    description: str

class OrderResponseShort (BaseModel) :
    id: int
    type: OrderType
    route_from: Governorate
    route_to: Governorate  


class OrderUpdateStatus (BaseModel ) : 
    status : OrderStatus


class Orderupdate (BaseModel) :
    type: OrderType| None = None
    operating_area :Governorate | None = None
    route_from: Governorate | None = None
    route_to: Governorate | None = None
    address_receive: str| None = None
    address_delivery:str| None = None
    description: str| None = None