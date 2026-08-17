from app.database.database import Base
from sqlalchemy import Column,Integer,ForeignKey,DateTime,func,Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.enums.route_enum import Governorate
from app.enums.trip import TripStatus

class Trip (Base) :
    __tablename__ = "trips"

    id = Column(
        Integer,
        primary_key=True,
        nullable= False
    )

    driver_id = Column(
        Integer,
        ForeignKey("drivers.id"),
        nullable=False
    )

    route_from = Column(
        SQLEnum(Governorate),
        nullable=False
    )

    route_to = Column(
        SQLEnum(Governorate),
        nullable=False
    )

    created_at = Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )

    status = Column(
            SQLEnum(TripStatus),
            default="planned",
            nullable=False
        )
    
    driver = relationship(
        "Driver",
        back_populates="trips"
    )

    orders = relationship(
        "Order",
        back_populates="trip",
    )