from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime, timedelta

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String(100), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)

    user = relationship("User", backref="password_reset_tokens")

    @staticmethod
    def generate_expiry():
        """Tokens expire in 15 minutes"""
        return datetime.utcnow() + timedelta(minutes=15)

    @staticmethod
    def generate_token():
        return str(uuid.uuid4())
