from pydantic import BaseModel, condecimal
from datetime import date, datetime
from typing import Optional


class SubscriptionBase(BaseModel):
    user_id: int
    server_id: int
    plan_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_renewal: Optional[bool] = False
    total_paid: condecimal(max_digits=10, decimal_places=2)


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    end_date: Optional[date] = None
    is_renewal: Optional[bool] = None
    total_paid: Optional[condecimal(max_digits=10, decimal_places=2)] = None


class SubscriptionResponse(SubscriptionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
