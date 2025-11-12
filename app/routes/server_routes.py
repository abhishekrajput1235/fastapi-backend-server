# app/routes/server_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.controllers import server_controller, payment_controller
from app.schemas import server_schemas, order_schemas
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/servers", tags=["Servers & Allocations"])

@router.post("/buy-server", status_code=status.HTTP_201_CREATED)
def buy_server_route(order: order_schemas.OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Buy a new server.
    This will create an order and a payment link.
    """
    return payment_controller.create_payment_order(db=db, order_details=order, user_id=current_user.id)


# ===============================================
# 1. Server Routes
# ===============================================

@router.post("/", response_model=server_schemas.ServerOut, status_code=status.HTTP_201_CREATED)
def create_server(server: server_schemas.ServerCreate, db: Session = Depends(get_db)):
    """Create a new server."""
    return server_controller.create_new_server(db=db, server=server)

@router.get("/", response_model=List[server_schemas.ServerOut])
def read_servers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all servers."""
    servers = server_controller.get_all_servers(db, skip=skip, limit=limit)
    return servers

@router.get("/{server_id}", response_model=server_schemas.ServerOut)
def read_server(server_id: int, db: Session = Depends(get_db)):
    """Retrieve a single server by its ID."""
    db_server = server_controller.get_server_by_id(db, server_id=server_id)
    if db_server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    return db_server

@router.put("/{server_id}", response_model=server_schemas.ServerOut)
def update_server(server_id: int, server: server_schemas.ServerUpdate, db: Session = Depends(get_db)):
    """Update an existing server."""
    return server_controller.update_existing_server(db=db, server_id=server_id, server_update=server)

@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_server(server_id: int, db: Session = Depends(get_db)):
    """Delete a server."""
    server_controller.delete_existing_server(db=db, server_id=server_id)
    return {"message": "Server deleted successfully"}

# ===============================================
# 2. Server-Plan Routes
# ===============================================

@router.post("/plans/", response_model=server_schemas.ServerPlanOut, status_code=status.HTTP_201_CREATED)
def add_plan_to_server_route(server_plan: server_schemas.ServerPlanCreate, db: Session = Depends(get_db)):
    """Associate a plan with a server."""
    return server_controller.add_plan_to_server(db=db, server_plan=server_plan)

@router.get("/{server_id}/plans", response_model=List[server_schemas.ServerPlanOut])
def get_server_plans_route(server_id: int, db: Session = Depends(get_db)):
    """Retrieve all plans for a specific server."""
    return server_controller.get_server_plans(db=db, server_id=server_id)

@router.delete("/plans/{server_plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_plan_from_server_route(server_plan_id: int, db: Session = Depends(get_db)):
    """Remove a plan's association from a server."""
    server_controller.remove_plan_from_server(db=db, server_plan_id=server_plan_id)
    return {"message": "Plan removed from server successfully"}

# ===============================================
# 3. Server Allocation Routes
# ===============================================

@router.post("/allocations/", response_model=server_schemas.ServerAllocationOut, status_code=status.HTTP_201_CREATED)
def create_allocation_route(allocation: server_schemas.ServerAllocationCreate, db: Session = Depends(get_db)):
    """Create a new server allocation."""
    return server_controller.create_new_allocation(db=db, allocation=allocation)

@router.get("/allocations/", response_model=List[server_schemas.ServerAllocationOut])
def read_allocations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all server allocations."""
    return server_controller.get_all_allocations(db, skip=skip, limit=limit)

@router.get("/allocations/{allocation_id}", response_model=server_schemas.ServerAllocationOut)
def read_allocation(allocation_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific server allocation by its ID."""
    return server_controller.get_allocation_by_id(db, allocation_id=allocation_id)

@router.get("/allocations/user/{user_id}", response_model=List[server_schemas.ServerAllocationOut])
def read_user_allocations(user_id: int, db: Session = Depends(get_db)):
    """Retrieve all allocations for a specific user."""
    return server_controller.get_allocations_by_user(db, user_id=user_id)

@router.delete("/allocations/{allocation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_allocation_route(allocation_id: int, db: Session = Depends(get_db)):
    """Delete a server allocation."""
    server_controller.delete_existing_allocation(db, allocation_id=allocation_id)
    return {"message": "Allocation deleted successfully"}