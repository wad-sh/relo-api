from app.enums.user_enum import UserEnum
from app.database.database import Base
from sqlalchemy import Column,String,Integer,Enum as SQLEnum
from sqlalchemy.orm import relationship

class User (Base) :
    __tablename__ = "users"
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    username= Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    phone_number = Column(
        String,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    role = Column(
        SQLEnum(UserEnum),
        default=UserEnum.Customer,
        nullable=False
    )

    orders_made = relationship(
        "Order",
        back_populates="order_owner",
    )

    applications = relationship(
            "DriverApplication",
            back_populates="applicant"
        )
    
    driver = relationship(
        "Driver",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    reviewed_applications = relationship(
            "DriverApplication",
            back_populates="reviewer"
        )