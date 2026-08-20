from app.database.database import Base
from sqlalchemy import Column,String,Integer,ForeignKey,DateTime,func,Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.enums.assignmentapplication import AssignmenApplicationtStatus

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
            SQLEnum(AssignmenApplicationtStatus),
            default="pending",
            nullable=False
        )

    responded_at = Column(
            DateTime(timezone=True),
            nullable= False
        )

    order = relationship(
        "Order",
        back_populates="assignmemts"
    )

    driver = relationship(
        "Driver",
        back_populates="assignmemts"
    )