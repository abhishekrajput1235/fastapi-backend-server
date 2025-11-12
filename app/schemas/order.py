from pydantic import BaseModel, condecimal
from typing import Optional, Dict, Any
from datetime import datetime

class OrderBase(BaseModel):
    user_id: int
    plan_id: int
    billing_cycle: str
    server_details: Optional[Dict[str, Any]] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    order_status: Optional[str] = None
    payment_status: Optional[str] = None
    payment_method: Optional[str] = None
    payment_reference: Optional[str] = None
    payment_date: Optional[datetime] = None

class OrderResponse(OrderBase):
    id: int
    order_number: str
    order_status: str
    payment_status: str
    total_amount: condecimal(max_digits=10, decimal_places=2)
    grand_total: condecimal(max_digits=10, decimal_places=2)
    created_at: datetime

    class Config:
        from_attributes = True
