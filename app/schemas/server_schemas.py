from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ServerPlanBase(BaseModel):
    plan_id: int
    price_override: Optional[float] = None

class ServerPlanCreate(ServerPlanBase):
    server_id: int

class ServerPlanOut(ServerPlanBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Updated for Pydantic v2
        # orm_mode = True  # old version

class ServerBase(BaseModel):
    name: str
    description: Optional[str] = None
    cpu: Optional[str] = None
    ram: Optional[str] = None
    storage: Optional[str] = None
    bandwidth: Optional[str] = None
    base_price: float
    is_active: Optional[bool] = True

class ServerCreate(ServerBase):
    pass

class ServerOut(ServerBase):
    id: int
    created_at: datetime
    server_plans: List[ServerPlanOut] = []

    class Config:
        from_attributes = True

class ServerAllocationBase(BaseModel):
    subscription_id: int
    user_id: int
    server_id: int
    ip_address: str
    username: str
    password: str
    status: Optional[str] = "active"

class ServerAllocationCreate(ServerAllocationBase):
    pass

class ServerAllocationOut(ServerAllocationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
