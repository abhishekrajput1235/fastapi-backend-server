from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.subscription import Subscription




class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    cpu = Column(String(100))
    ram = Column(String(50))
    storage = Column(String(100))
    bandwidth = Column(String(50))
    base_price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # ✅ Add this line (fixes your error)
    subscriptions = relationship("Subscription", back_populates="server", cascade="all, delete-orphan")

    # Other relationships
    server_plans = relationship("ServerPlan", back_populates="server", cascade="all, delete-orphan")
    allocations = relationship("ServerAllocation", back_populates="server", cascade="all, delete-orphan")


class ServerPlan(Base):
    __tablename__ = "server_plans"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer, ForeignKey("servers.id", ondelete="CASCADE"))
    plan_id = Column(Integer, ForeignKey("plans.id", ondelete="CASCADE"))
    price_override = Column(Numeric(10, 2))
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    server = relationship("Server", back_populates="server_plans")
    plan = relationship("Plan", back_populates="server_plans")


class ServerAllocation(Base):
    __tablename__ = "server_allocations"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    server_id = Column(Integer, ForeignKey("servers.id", ondelete="CASCADE"))
    ip_address = Column(String(45))
    username = Column(String(100))
    password = Column(String(100))
    status = Column(String(20), default="active")
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    server = relationship("Server", back_populates="allocations")
    user = relationship("User")
    subscription = relationship("Subscription")
