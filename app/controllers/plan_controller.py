# app/controllers/plan_controller.py
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.plan import Plan
from app.schemas.plan import PlanCreate, PlanUpdate

def create_new_plan(db: Session, plan: PlanCreate) -> Plan:
    """Create a new plan."""
    db_plan = Plan(**plan.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def get_all_plans(db: Session, skip: int = 0, limit: int = 100) -> List[Plan]:
    """Retrieve all plans with pagination."""
    return db.query(Plan).offset(skip).limit(limit).all()

def get_plan_by_id(db: Session, plan_id: int) -> Plan:
    """Retrieve a single plan by its ID."""
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    return plan

def update_existing_plan(db: Session, plan_id: int, plan_update: PlanUpdate) -> Plan:
    """Update an existing plan."""
    db_plan = get_plan_by_id(db, plan_id)
    update_data = plan_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_plan, key, value)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def delete_existing_plan(db: Session, plan_id: int) -> None:
    """Delete a plan."""
    db_plan = get_plan_by_id(db, plan_id)
    db.delete(db_plan)
    db.commit()
