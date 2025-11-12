# app/controllers/order_controller.py
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.plan import Plan
from app.schemas.order import OrderCreate
import uuid

def create_order(db: Session, order: OrderCreate, user_id: int):
    plan = db.query(Plan).filter(Plan.id == order.plan_id).first()
    if not plan:
        return None

    order_number = str(uuid.uuid4())
    total_amount = plan.price
    grand_total = total_amount

    db_order = Order(
        user_id=user_id,
        plan_id=order.plan_id,
        order_number=order_number,
        billing_cycle=order.billing_cycle,
        total_amount=total_amount,
        grand_total=grand_total,
        server_details=order.server_details
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
