from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers import payment_controller

router = APIRouter()

@router.post("/payments/verify")
async def verify_payment_route(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    razorpay_order_id = form_data.get("razorpay_order_id")
    razorpay_payment_id = form_data.get("razorpay_payment_id")
    razorpay_signature = form_data.get("razorpay_signature")
    
    return payment_controller.verify_payment(
        db=db,
        razorpay_order_id=razorpay_order_id,
        razorpay_payment_id=razorpay_payment_id,
        razorpay_signature=razorpay_signature,
    )

