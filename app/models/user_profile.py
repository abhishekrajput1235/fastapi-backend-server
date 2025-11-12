from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class UserProfile(Base):
    __tablename__ = "users_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")
    account_status = Column(String(50), nullable=False, default="active")
    hashed_password = Column(String(255), nullable=False)
    referral_code = Column(String(50), unique=True)
    referred_by = Column(Integer, ForeignKey("users_profiles.id"), nullable=True)
    referral_level_1 = Column(Integer, ForeignKey("users_profiles.id"), nullable=True)
    referral_level_2 = Column(Integer, ForeignKey("users_profiles.id"), nullable=True)
    referral_level_3 = Column(Integer, ForeignKey("users_profiles.id"), nullable=True)

    # ✅ Referral stats
    total_referrals = Column(Integer, default=0)
    l1_referrals = Column(Integer, default=0)
    l2_referrals = Column(Integer, default=0)
    l3_referrals = Column(Integer, default=0)

    # ✅ Earnings
    total_earnings = Column(Numeric(10, 2), default=0.00)
    available_balance = Column(Numeric(10, 2), default=0.00)
    total_withdrawn = Column(Numeric(10, 2), default=0.00)

    # ✅ Extra profile info
    phone = Column(String(20), nullable=True)
    company = Column(String(255), nullable=True)
    subscription_status = Column(String(50), nullable=True)
    subscription_start = Column(DateTime(timezone=False), nullable=True)
    subscription_end = Column(DateTime(timezone=False), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
