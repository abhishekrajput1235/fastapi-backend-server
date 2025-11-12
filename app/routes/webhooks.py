# app/routes/webhooks.py
from fastapi import APIRouter, Request, Header, HTTPException, status, Depends
from sqlalchemy.orm import Session
import hmac
import hashlib
import os
import logging
from datetime import datetime
from app.core.database import get_db
from app.models.payment import Payment

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET")
logger = logging.getLogger("webhooks")

def verify_razorpay_signature(body_bytes: bytes, header_signature: str, secret: str) -> bool:
    """Verify Razorpay webhook signature. Returns True if valid."""
    if not header_signature or not secret:
        return False
    computed = hmac.new(secret.encode("utf-8"), body_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, header_signature)

@router.post("/razorpay")
async def razorpay_webhook(
    request: Request,
    x_razorpay_signature: str = Header(None),
    db: Session = Depends(get_db),
):
    body_bytes = await request.body()

    # Verify signature
    if not verify_razorpay_signature(body_bytes, x_razorpay_signature, RAZORPAY_WEBHOOK_SECRET):
        logger.warning("Invalid webhook signature")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook signature")

    # Parse payload safely
    try:
        payload = await request.json()
    except Exception:
        logger.exception("Invalid JSON payload in webhook")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON payload")

    # Extract payment entity robustly
    payment_entity = (
        payload.get("payload", {})
               .get("payment", {})
               .get("entity", {})
    ) or {}

    # get fields (Razorpay amounts are in paise)
    razorpay_payment_id = payment_entity.get("id")
    razorpay_order_id = payment_entity.get("order_id")
    raw_amount = payment_entity.get("amount")  # paise
    try:
        amount = (int(raw_amount) / 100.0) if raw_amount is not None else None
    except Exception:
        amount = None

    status_text = payment_entity.get("status")  # e.g., 'captured','failed','created'
    mapped_status = "pending"
    if status_text in ("captured", "authorized"):
        mapped_status = "completed"
    elif status_text in ("failed",):
        mapped_status = "failed"

    # Try finding matching payment row by stored order id (transaction_id)
    payment_row = None
    if razorpay_order_id:
        payment_row = db.query(Payment).filter(Payment.transaction_id == razorpay_order_id).first()
    # fallback: maybe we stored razorpay_order_id in explicit column
    if not payment_row and hasattr(Payment, "razorpay_order_id") and razorpay_order_id:
        payment_row = db.query(Payment).filter(Payment.razorpay_order_id == razorpay_order_id).first()
    # fallback: match by razorpay_payment_id column
    if not payment_row and razorpay_payment_id and hasattr(Payment, "razorpay_payment_id"):
        payment_row = db.query(Payment).filter(Payment.razorpay_payment_id == razorpay_payment_id).first()

    if not payment_row:
        logger.info("Webhook verified but no matching payment row found", extra={"order_id": razorpay_order_id})
        # 200 OK so Razorpay doesn't keep retrying for a missing-order scenario.
        return {"status": "ignored", "detail": "payment record not found"}

    # Idempotency: if already completed, ignore
    if payment_row.payment_status == "completed":
        logger.info("Payment already completed; ignoring duplicate webhook", extra={"payment_id": payment_row.id})
        return {"status": "ignored", "detail": "already processed"}

    # Optional: amount verification — ensure webhook amount matches DB expected amount
    if amount is not None and float(payment_row.amount) != float(amount):
        logger.warning("Webhook amount does not match DB amount",
                       extra={"db_amount": str(payment_row.amount), "webhook_amount": amount})
        # you can choose to reject or continue; here we log and continue but mark as failed for safety
        # raise HTTPException(status_code=400, detail="Amount mismatch")

    # Update payment row
    payment_row.transaction_id = razorpay_payment_id or payment_row.transaction_id
    # Optionally populate explicit columns if present
    if hasattr(payment_row, "razorpay_order_id") and razorpay_order_id:
        payment_row.razorpay_order_id = razorpay_order_id
    if hasattr(payment_row, "razorpay_payment_id") and razorpay_payment_id:
        payment_row.razorpay_payment_id = razorpay_payment_id

    payment_row.payment_method = payment_entity.get("method") or payment_row.payment_method
    payment_row.amount = amount if amount is not None else payment_row.amount
    payment_row.payment_status = mapped_status
    if mapped_status == "completed":
        payment_row.payment_date = datetime.utcnow()

    db.add(payment_row)
    db.commit()

    logger.info("Payment updated from webhook", extra={"payment_db_id": payment_row.id, "status": mapped_status})
    # DB triggers (if configured) will run after this UPDATE and handle subscriptions/commissions/referral activation
    return {"status": "ok"}
