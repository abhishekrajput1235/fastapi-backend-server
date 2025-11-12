from sqlalchemy import Column, Integer, ForeignKey, Numeric, Boolean, Date, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    server_id = Column(Integer, ForeignKey("servers.id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(Date, server_default=func.current_date())
    end_date = Column(Date)
    is_renewal = Column(Boolean, default=False)
    total_paid = Column(Numeric(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="subscriptions")
    server = relationship("Server", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")
