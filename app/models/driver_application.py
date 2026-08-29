from app.database.database import Base
from sqlalchemy import Column,String,Integer,ForeignKey,DateTime,func,Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.enums.application import ApplicationStatus,VehicleType
from app.enums.route_enum import Governorate

class DriverApplication (Base) :
    __tablename__ = "drivers_applications"

    id = Column(
                Integer,
                primary_key=True,
        index=True
            )

    applicant_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    created_at = Column(
                    DateTime(timezone=True),
                    server_default=func.now(),
                    nullable=False
                )
    
    reviewed_at = Column(
            DateTime(timezone=True)
        )
    
    reviewed_by = Column(
        Integer,
        ForeignKey("users.id"),
    )
    
    status = Column(
        SQLEnum(ApplicationStatus),
        default=ApplicationStatus.PENDING,
        nullable=False
    )

    vehicle_type=Column(
        SQLEnum(VehicleType),
        nullable=False
    )

    vehicle_model=Column(
        String,nullable=False
    )

    vehicle_year=Column(
        Integer,
        nullable=False
    )

    vehicle_capacity_kg=Column(
        Integer,
        nullable=False
    )

    preferred_area = Column(
        SQLEnum(Governorate),
        nullable=False
        )

    preferred_route_from = Column(
        SQLEnum(Governorate)
    )

    preferred_route_to =Column(
        SQLEnum(Governorate)
    )

    description=Column(
        String
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