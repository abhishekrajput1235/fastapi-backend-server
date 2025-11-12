from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, JSON, DateTime, func
from app.core.database import Base
from sqlalchemy.orm import relationship

class HostingPlan(Base):
    __tablename__ = "hosting_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    plan_type = Column(String(50), nullable=False)
    cpu_cores = Column(Integer, nullable=False)
    ram_gb = Column(Integer, nullable=False)
    storage_gb = Column(Integer, nullable=False)
    bandwidth_gb = Column(Integer, nullable=False)
    base_price = Column(Numeric(10, 2), nullable=False)
    monthly_price = Column(Numeric(10, 2), nullable=False)
    quarterly_price = Column(Numeric(10, 2), nullable=False)
    annual_price = Column(Numeric(10, 2), nullable=False)
    biennial_price = Column(Numeric(10, 2), nullable=False)
    triennial_price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    features = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    orders = relationship("Order", back_populates="plan")
