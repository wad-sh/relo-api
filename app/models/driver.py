from app.database.database import Base
from sqlalchemy import Column,Integer,ForeignKey,Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.enums.driver_modes import DrivingMode
from app.enums.route_enum import Governorate

class Driver (Base) :
    __tablename__ = "drivers"

    id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True,
        nullable= False,
        index=True
    )

    mode = Column(
        SQLEnum(DrivingMode),
        default=DrivingMode.FLEXIBLE,
        nullable= False
    )

    local_operating_area = Column(
        SQLEnum(Governorate),
        index=True
    )

    assignments = relationship(
                "DriverAssignment",
                back_populates="driver"
            )
    
    user = relationship(
        "User",
        back_populates="driver"
    )

    trips = relationship(
        "Trip",
        back_populates="driver",
    )

    orders_for_driver = relationship(
        "Order",
        back_populates="driver"
    )
