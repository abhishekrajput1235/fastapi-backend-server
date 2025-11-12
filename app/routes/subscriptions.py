from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.core.database import get_db
from app.models.subscription import Subscription
from app.models.plan import Plan
from app.models.server import Server

router = APIRouter()

@router.post("/subscriptions/create")
def create_subscription(user_id: int, server_id: int, plan_id: int, db: Session = Depends(get_db)):
    server = db.query(Server).filter(Server.id==server_id).first()
    plan = db.query(Plan).filter(Plan.id==plan_id).first()
    if not server or not plan:
        raise HTTPException(404, "Server or Plan not found")
    end_date = None
    if plan.duration_months:
        end_date = date.today() + timedelta(days=plan.duration_months*30)
    sub = Subscription(
        user_id=user_id, server_id=server_id, plan_id=plan_id,
        start_date=date.today(), end_date=end_date, total_paid=0.00, is_renewal=False
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return {"subscription_id": sub.id, "price": float(plan.price)}
