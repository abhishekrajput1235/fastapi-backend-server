from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user import UserCreate, UserLogin
import uuid
from datetime import datetime, timedelta
import secrets
from app.utils.email_utils import send_email  # 👈 you’ll create this utility

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory token store (for demo — use Redis or DB in production)
reset_tokens = {}

# ===============================
# 🔐 Password Hashing Utilities
# ===============================
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ===============================
# 🧾 Signup Controller
# ===============================
def signup_controller(user: UserCreate, db: Session):
    """Registers a new user and creates a default user profile."""
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    referral_code = str(uuid.uuid4())[:8].upper()

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
        referrer_id=user.referrer_id if user.referrer_id else None,
        referral_code=referral_code
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create matching profile
    user_profile = UserProfile(
        email=new_user.email,
        full_name=new_user.name,
        role="user",
        account_status="active",
        hashed_password=new_user.password_hash,
        referral_code=new_user.referral_code,
        referred_by=new_user.referrer_id,
        total_referrals=0,
        l1_referrals=0,
        l2_referrals=0,
        l3_referrals=0,
        total_earnings=0.00,
        available_balance=0.00,
        total_withdrawn=0.00,
    )

    db.add(user_profile)
    db.commit()

    return {
        "message": "Signup successful",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "name": new_user.name,
            "referral_code": new_user.referral_code,
            "role": user_profile.role,
        }
    }


# ===============================
# 🔓 Login Controller
# ===============================
def login_controller(user: UserLogin, db: Session):
    """Authenticates user and returns profile details with role."""
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    profile = db.query(UserProfile).filter(UserProfile.email == db_user.email).first()
    role = profile.role if profile else "user"

    return {
        "message": "Login successful",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "name": db_user.name,
            "role": role,
            "referral_code": db_user.referral_code,
        }
    }


# ===============================
# 🔄 Request Password Reset
# ===============================
def request_password_reset(email: str, db: Session):
    """Generates reset token and sends email link."""
    user = db.query(UserProfile).filter(UserProfile.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=30)

    # Save token temporarily
    reset_tokens[email] = {"token": token, "expires_at": expires_at}

    reset_link = f"https://your-frontend.com/reset-password?token={token}&email={email}"

    # send email (mock/demo)
    send_email(
        to_email=email,
        subject="Password Reset Request",
        body=f"Click the link to reset your password:\n{reset_link}\nThis link expires in 30 minutes."
    )

    return {"message": "Password reset email sent successfully"}


# ===============================
# 🔁 Reset Password
# ===============================
def reset_password(email: str, token: str, new_password: str, db: Session):
    """Validates token and updates password in both tables."""
    if email not in reset_tokens:
        raise HTTPException(status_code=400, detail="Reset token not found")

    token_data = reset_tokens[email]
    if token_data["token"] != token:
        raise HTTPException(status_code=400, detail="Invalid reset token")

    if datetime.utcnow() > token_data["expires_at"]:
        raise HTTPException(status_code=400, detail="Token expired")

    # ✅ Update password in users and user_profiles tables
    hashed = hash_password(new_password)

    user = db.query(User).filter(User.email == email).first()
    if user:
        user.password_hash = hashed

    profile = db.query(UserProfile).filter(UserProfile.email == email).first()
    if profile:
        profile.hashed_password = hashed

    db.commit()

    # Remove token after use
    del reset_tokens[email]

    return {"message": "Password reset successful"}
