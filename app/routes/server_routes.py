from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app import schemas, controllers


router = APIRouter(prefix="/servers", tags=["Servers"])

@router.post("/", response_model=schemas.ServerOut)
def create_server(server: schemas.ServerCreate, db: Session = Depends(get_db)):
    return controllers.server_controller.create_server(db, server)

@router.get("/", response_model=list[schemas.ServerOut])
def list_servers(db: Session = Depends(get_db)):
    return controllers.server_controller.get_servers(db)

@router.get("/{server_id}", response_model=schemas.ServerOut)
def get_server(server_id: int, db: Session = Depends(get_db)):
    server = controllers.server_controller.get_server(db, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server

@router.post("/plans", response_model=schemas.ServerPlanOut)
def add_plan(plan: schemas.ServerPlanCreate, db: Session = Depends(get_db)):
    return controllers.server_controller.add_server_plan(db, plan)

@router.post("/allocations", response_model=schemas.ServerAllocationOut)
def allocate_server(allocation: schemas.ServerAllocationCreate, db: Session = Depends(get_db)):
    return controllers.server_controller.create_allocation(db, allocation)
