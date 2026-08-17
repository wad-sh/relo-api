from app.database.database import Base
from sqlalchemy import Column,String,Integer,ForeignKey,DateTime,func,Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.enums.assignmentapplication import AssignmenApplicationtStatus

class DriverApplication (Base) :
    __tablename__ = "drivers_applications"

    id = Column(
                Integer,
                primary_key=True
            )

    applicant_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    
    created_at = Column(
                    DateTime(timezone=True),
                    server_default=func.now(),
                    nullable=False
                )
    
    last_status_change = Column(
            DateTime(timezone=True)
        )
    
    reviewed_by = Column(
        Integer,
        ForeignKey("users.id")
    )
    
    status = Column(
        SQLEnum(AssignmenApplicationtStatus),
        default="pending",
        nullable=False
    )

    applicant = relationship(
        "User",
        back_populates="applications",
        foreign_keys=[applicant_id]
    )

    reviewer = relationship(
            "User",
            back_populates="reviewed_applications",
            foreign_keys=[reviewed_by]
        )