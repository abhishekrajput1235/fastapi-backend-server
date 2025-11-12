from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    amount = Column(Numeric(10,2), nullable=False)
    payment_method = Column(String(50))
    payment_status = Column(String(20))  # pending/completed/failed
    transaction_id = Column(String(200))  # will store razorpay order_id initially, then payment_id
    payment_date = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    notes = Column(JSON)
