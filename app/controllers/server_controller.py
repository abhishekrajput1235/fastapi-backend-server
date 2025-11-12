# app/controllers/server_controller.py
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.models.server import Server, ServerPlan, ServerAllocation
from app.models.plan import Plan
from app.schemas.server_schemas import (
    ServerCreate, ServerUpdate, ServerPlanCreate, ServerAllocationCreate
)
from app.schemas.order import OrderCreate
from app.controllers.order_controller import create_order as create_order_logic
import razorpay
import os
from app.models.payment import Payment
from datetime import datetime

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))





# ===============================================
# 1. Server Operations
# ===============================================

def create_new_server(db: Session, server: ServerCreate) -> Server:
    """Create a new server and associate it with plans."""
    # Extract server_plans from the input schema
    server_plans_data = server.server_plans
    server_data = server.model_dump(exclude={"server_plans"})

    # Create the server
    db_server = Server(**server_data)
    db.add(db_server)
    db.flush()  # Flush to get the server.id before committing

    # Create and associate server plans
    for sp_data in server_plans_data:
        # Check if the plan_id exists
        plan = db.query(Plan).filter(Plan.id == sp_data.plan_id).first()
        if not plan:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Plan with ID {sp_data.plan_id} not found")

        db_server_plan = ServerPlan(
            server_id=db_server.id,
            plan_id=sp_data.plan_id,
            price_override=sp_data.price_override
        )
        db.add(db_server_plan)

    db.commit()
    db.refresh(db_server)
    return db_server

def get_all_servers(db: Session, skip: int = 0, limit: int = 100) -> List[Server]:
    """Retrieve all servers with pagination."""
    return db.query(Server).offset(skip).limit(limit).all()

def get_server_by_id(db: Session, server_id: int) -> Server:
    """Retrieve a single server by its ID."""
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found")
    return server

def update_existing_server(db: Session, server_id: int, server_update: ServerUpdate) -> Server:
    """Update an existing server."""
    db_server = get_server_by_id(db, server_id)
    update_data = server_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_server, key, value)
    db.commit()
    db.refresh(db_server)
    return db_server

def delete_existing_server(db: Session, server_id: int) -> None:
    """Delete a server."""
    db_server = get_server_by_id(db, server_id)
    db.delete(db_server)
    db.commit()

# ===============================================
# 2. Server-Plan Operations
# ===============================================

def add_plan_to_server(db: Session, server_plan: ServerPlanCreate) -> ServerPlan:
    """Associate a plan with a server."""
    # Ensure server and plan exist
    get_server_by_id(db, server_plan.server_id)
    plan = db.query(Plan).filter(Plan.id == server_plan.plan_id).first()
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    
    db_server_plan = ServerPlan(**server_plan.model_dump())
    db.add(db_server_plan)
    db.commit()
    db.refresh(db_server_plan)
    return db_server_plan

def get_server_plans(db: Session, server_id: int) -> List[ServerPlan]:
    """Retrieve all plans associated with a specific server."""
    server = db.query(Server).options(joinedload(Server.server_plans)).filter(Server.id == server_id).first()
    if not server:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found")
    return server.server_plans

def remove_plan_from_server(db: Session, server_plan_id: int) -> None:
    """Remove a plan's association from a server."""
    db_server_plan = db.query(ServerPlan).filter(ServerPlan.id == server_plan_id).first()
    if not db_server_plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server-plan link not found")
    db.delete(db_server_plan)
    db.commit()

# ===============================================
# 3. Server Allocation Operations
# ===============================================

def create_new_allocation(db: Session, allocation: ServerAllocationCreate) -> ServerAllocation:
    """Create a new server allocation for a user's subscription."""
    db_allocation = ServerAllocation(**allocation.model_dump())
    db.add(db_allocation)
    db.commit()
    db.refresh(db_allocation)
    return db_allocation

def get_all_allocations(db: Session, skip: int = 0, limit: int = 100) -> List[ServerAllocation]:
    """Retrieve all server allocations."""
    return db.query(ServerAllocation).offset(skip).limit(limit).all()

def get_allocation_by_id(db: Session, allocation_id: int) -> ServerAllocation:
    """Retrieve a specific server allocation by its ID."""
    allocation = db.query(ServerAllocation).filter(ServerAllocation.id == allocation_id).first()
    if not allocation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allocation not found")
    return allocation

def get_allocations_by_user(db: Session, user_id: int) -> List[ServerAllocation]:
    """Retrieve all server allocations for a specific user."""
    return db.query(ServerAllocation).filter(ServerAllocation.user_id == user_id).all()

def delete_existing_allocation(db: Session, allocation_id: int) -> None:
    """Delete a server allocation."""
    db_allocation = get_allocation_by_id(db, allocation_id)
    db.delete(db_allocation)
    db.commit()