from app.enums.user_enum import UserEnum
from app.database.database import Base
from sqlalchemy import Column,String,Integer,Enum as SQLEnum
from sqlalchemy.orm import relationship

class User (Base) :
    __tablename__ = "users"
    id = Column(
        Integer,
        primary_key=True
    )
    username= Column(
        String,
        unique=True,
        nullable=False
    )

    email= Column(
            String,
            unique=True,
            nullable=False
        )

    hashed_password = Column(
        String,
        nullable=False
    )

    role = Column(
        SQLEnum(UserEnum),
        nullable=False
    )

    orders = relationship(
        "Order",
        back_populates="order_owner"
    )

    user_orders_history = relationship(
        "HistoryOrder",
        back_populates="order_owner"
    )

    applications = relationship(
            "DriverApplication",
            back_populates="applicant"
        )
    
    driver = relationship(
        "Driver",
        back_populates="user",
        uselist=False
    )