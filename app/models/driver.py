from app.database.database import Base
from sqlalchemy import Column,Integer,ForeignKey,Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.enums.route_enum import Governorate


class Driver (Base) :
    __tablename__ = "drivers"

    id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True,
        nullable= False
    )

    governorate_1 = Column(
        SQLEnum(Governorate),
        nullable= False
    )

    governorate_2 = Column(
            SQLEnum(Governorate),
            nullable= False
        )

    assignments = relationship(
                "DriverAssignment",
                back_populates="driver"
            )
    user = relationship(
        "User",
        back_populates="driver",
        uselist=False
    )