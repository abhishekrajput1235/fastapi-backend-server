from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.controllers.auth_controller import (
    signup_controller,
    login_controller,
    request_password_reset,
    reset_password,
)
from app.schemas.user import UserCreate, UserLogin
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return signup_controller(user, db)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_controller(user, db)

@router.post("/request-password-reset")
def request_reset(email: str = Body(...), db: Session = Depends(get_db)):
    return request_password_reset(email, db)

@router.post("/reset-password")
def reset_pass(
    email: str = Body(...),
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(get_db)
):
    return reset_password(email, token, new_password, db)
