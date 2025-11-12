from pydantic import BaseModel, condecimal, Field
from typing import Optional, Literal
from datetime import datetime


class PlanBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    duration_months: Optional[int] = None
    price: condecimal(max_digits=10, decimal_places=2)
    commission_type: Literal["recurring", "one-time", "activation"]


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_months: Optional[int] = None
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    commission_type: Optional[Literal["recurring", "one-time", "activation"]] = None


class PlanResponse(PlanBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
