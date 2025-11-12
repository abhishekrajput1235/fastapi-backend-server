from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.subscription import Subscription
from app.models.plan import Plan
from app.models.payment import Payment
import os, razorpay
from datetime import datetime

router = APIRouter()
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@router.post("/payments/create-order")
def create_order(subscription_id: int, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id==subscription_id).first()
    if not sub:
        raise HTTPException(404, "Subscription not found")
    plan = db.query(Plan).filter(Plan.id==sub.plan_id).first()
    if not plan:
        raise HTTPException(404, "Plan not found")
    amount_paise = int(float(plan.price) * 100)
    order = client.order.create({"amount": amount_paise, "currency":"INR","payment_capture":1, "notes":{"subscription_id": subscription_id}})
    # Save pending payment with transaction_id = razorpay order id
    payment = Payment(
        user_id=sub.user_id,
        subscription_id=sub.id,
        amount=plan.price,
        payment_method="razorpay",
        payment_status="pending",
        transaction_id=order["id"],
        payment_date=datetime.utcnow()
    )
    db.add(payment); db.commit(); db.refresh(payment)
    return {"order_id": order["id"], "amount": float(plan.price), "key": RAZORPAY_KEY_ID, "payment_db_id": payment.id}
