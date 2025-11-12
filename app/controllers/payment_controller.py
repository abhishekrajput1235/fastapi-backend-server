# app/controllers/payment_controller.py
from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.models.order import Order
from app.models.subscription import Subscription
from app.models.server import ServerAllocation
from app.models.user import User
from app.models.plan import Plan
import razorpay
import os
from datetime import date, timedelta

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def verify_payment(db: Session, razorpay_order_id: str, razorpay_payment_id: str, razorpay_signature: str):
    # Verify the payment signature
    try:
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        razorpay_client.utility.verify_payment_signature(params_dict)
    except razorpay.errors.SignatureVerificationError:
        return {"status": "error", "message": "Invalid payment signature"}

    # Update payment status
    payment = db.query(Payment).filter(Payment.transaction_id == razorpay_order_id).first()
    if not payment:
        return {"status": "error", "message": "Payment record not found"}

    payment.payment_status = "completed"
    payment.transaction_id = razorpay_payment_id
    db.commit()

    # Update order status
    order = db.query(Order).filter(Order.id == payment.notes["order_id"]).first()
    if not order:
        return {"status": "error", "message": "Order not found"}

    order.payment_status = "completed"
    order.order_status = "completed"
    order.payment_reference = razorpay_payment_id
    db.commit()

    # Create subscription
    plan = db.query(Plan).filter(Plan.id == order.plan_id).first()
    end_date = None
    if plan.duration_months:
        end_date = date.today() + timedelta(days=plan.duration_months * 30)

    subscription = Subscription(
        user_id=order.user_id,
        server_id=order.server_details["server_id"],
        plan_id=order.plan_id,
        start_date=date.today(),
        end_date=end_date,
        total_paid=order.grand_total,
        is_renewal=False
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    # Allocate server
    server_allocation = ServerAllocation(
        subscription_id=subscription.id,
        user_id=order.user_id,
        server_id=order.server_details["server_id"],
        status="active"
    )
    db.add(server_allocation)
    db.commit()

    return {"status": "success", "message": "Payment verified and subscription created"}
