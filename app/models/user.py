from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    referral_code = Column(String(20), unique=True, index=True)
    is_referral_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

