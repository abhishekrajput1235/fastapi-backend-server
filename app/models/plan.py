from sqlalchemy import Column, Integer, String, Numeric, Text, TIMESTAMP, func, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    duration_months = Column(Integer)
    price = Column(Numeric(10, 2), nullable=False)
    commission_type = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "commission_type IN ('recurring', 'one-time', 'activation')",
            name="plans_commission_type_check"
        ),
    )

    # Relationships
    subscriptions = relationship("Subscription", back_populates="plan", cascade="all, delete-orphan")
    server_plans = relationship("ServerPlan", back_populates="plan", cascade="all, delete-orphan")
