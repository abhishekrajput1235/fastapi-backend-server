# app/routes/user_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.user_controller import get_all_users, get_user_by_id

router = APIRouter(prefix="/users", tags=["Users"])

# ✅ Get all users
@router.get("/get-all-users")
def fetch_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)

# ✅ Get a single user by ID
@router.get("/{user_id}")
def fetch_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(user_id, db)
