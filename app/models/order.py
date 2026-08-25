from app.database.database import Base
from sqlalchemy import Column,String,Integer,ForeignKey,DateTime,func,Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.enums.order import OrderStatus,OrderType
from app.enums.route_enum import Governorate

class Order (Base) :
    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        index=True
    )

    order_owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    status = Column(
        SQLEnum(OrderStatus),
        default="pending",
        nullable=False
    )

    type = Column(
        SQLEnum(OrderType),
        nullable=False
    )

    operating_area = Column(
        SQLEnum(Governorate),
        index=True
    )

    route_from =Column(
        SQLEnum(Governorate),
        index=True
    )

    route_to =Column(
        SQLEnum(Governorate),
        index=True
    )

    address_receive = Column(
        String,
        nullable=False
    )

    address_delivery = Column(
            String,
            nullable=False
        )

    description = Column(
        String,
        nullable=False
    )

    trip_id =Column(
        Integer,
        ForeignKey("trips.id")
    )

    driver_id = Column(
        Integer,
        ForeignKey("drivers.id")
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    order_owner = relationship(
        "User",
        back_populates="orders_made"
    )

    driver = relationship(
        "Driver",
        back_populates="orders_for_driver"
    )

    trip =relationship(
        "Trip",
        back_populates="orders"
    )

    order_history= relationship(
        "HistoryOrder",
        back_populates="order",
    )

    assignmemts = relationship(
        "DriverAssignment",
        back_populates="order",
        cascade="all, delete-orphan"
    )