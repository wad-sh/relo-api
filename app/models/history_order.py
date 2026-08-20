from app.database.database import Base
from sqlalchemy import Column,String,Integer,ForeignKey,DateTime,Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.enums.order import OrderStatus,OrderType
from app.enums.route_enum import Governorate

class HistoryOrder (Base) :
    __tablename__ = "orders_history"

    id = Column(
            Integer,
            primary_key=True,
        index=True
        )

    order_id =Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False,
        index=True
    )

    old_status = Column(
        SQLEnum(OrderStatus),
        nullable=False
    )

    new_status = Column(
            SQLEnum(OrderStatus),
            nullable=False
        )

    changed_at = Column(
        DateTime(timezone=True),
        nullable= False
    )

    changed_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    more_details = Column(
        String
    )

    order = relationship(
        "Order",
        back_populates="order_history"
    )