from app.database.database import Base
from sqlalchemy import Column,String,Integer,ForeignKey,DateTime,func,Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.enums.assignment import AssignmentStatus

class DriverAssignment (Base) :
    __tablename__ = "drivers_assignments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id = Column(
            Integer,
            ForeignKey("orders.id"),
            nullable=False,
        index=True
        )
    
    driver_id = Column(
        Integer,
        ForeignKey("drivers.id"),
        nullable=False,
        index=True
    )

    created_at = Column(
                DateTime(timezone=True),
                server_default=func.now(),
                nullable=False
            )

    status = Column(
            SQLEnum(AssignmentStatus),
            default=AssignmentStatus.WAITING,
            nullable=False
        )

    responded_at = Column(
            DateTime(timezone=True)
        )

    order = relationship(
        "Order",
        back_populates="assignments"
    )

    driver = relationship(
        "Driver",
        back_populates="assignments"
    )