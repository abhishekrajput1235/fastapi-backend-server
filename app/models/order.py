from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, func, JSON
from app.core.database import Base
from sqlalchemy.orm import relationship
from app.models.user import User
from app.models.plan import Plan
from app.models.server import Server

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    server_id = Column(Integer, ForeignKey("servers.id"), nullable=False)
    order_number = Column(String(100), unique=True, nullable=False)
    order_status = Column(String(50), default="pending")
    payment_status = Column(String(50), default="pending")
    billing_cycle = Column(String(50), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0.0)
    tax_amount = Column(Numeric(10, 2), default=0.0)
    grand_total = Column(Numeric(10, 2))
    payment_method = Column(String(100))
    payment_reference = Column(String(255))
    payment_date = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship("User", back_populates="orders")
    plan = relationship("Plan")
    server = relationship("Server")
