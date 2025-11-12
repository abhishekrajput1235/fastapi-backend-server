# app/controllers/user_controller.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User

# ✅ Get all users
def get_all_users(db: Session):
    users = db.query(User).all()
    return users

# ✅ Get a single user by ID
def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
