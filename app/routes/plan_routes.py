# app/routes/plan_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.controllers import plan_controller
from app.schemas import plan as plan_schema

router = APIRouter(prefix="/plans", tags=["Plans"])

@router.post("/", response_model=plan_schema.PlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(plan: plan_schema.PlanCreate, db: Session = Depends(get_db)):
    """Create a new plan."""
    return plan_controller.create_new_plan(db=db, plan=plan)

@router.get("/", response_model=List[plan_schema.PlanResponse])
def read_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all plans."""
    plans = plan_controller.get_all_plans(db, skip=skip, limit=limit)
    return plans

@router.get("/{plan_id}", response_model=plan_schema.PlanResponse)
def read_plan(plan_id: int, db: Session = Depends(get_db)):
    """Retrieve a single plan by its ID."""
    db_plan = plan_controller.get_plan_by_id(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return db_plan

@router.put("/{plan_id}", response_model=plan_schema.PlanResponse)
def update_plan(plan_id: int, plan: plan_schema.PlanUpdate, db: Session = Depends(get_db)):
    """Update an existing plan."""
    return plan_controller.update_existing_plan(db=db, plan_id=plan_id, plan_update=plan)

@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    """Delete a plan."""
    plan_controller.delete_existing_plan(db=db, plan_id=plan_id)
    return {"message": "Plan deleted successfully"}
