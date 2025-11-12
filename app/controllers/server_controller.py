from sqlalchemy.orm import Session
from app import models, schemas


# -------------------- SERVERS --------------------
def create_server(db: Session, server: schemas.ServerCreate):
    db_server = models.Server(**server.dict())
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server


def get_servers(db: Session):
    return db.query(models.Server).all()


def get_server(db: Session, server_id: int):
    return db.query(models.Server).filter(models.Server.id == server_id).first()


# -------------------- SERVER PLANS --------------------
def add_server_plan(db: Session, plan: schemas.ServerPlanCreate):
    db_plan = models.ServerPlan(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


def get_server_plans(db: Session, server_id: int):
    return db.query(models.ServerPlan).filter(models.ServerPlan.server_id == server_id).all()


# -------------------- SERVER ALLOCATIONS --------------------
def create_allocation(db: Session, allocation: schemas.ServerAllocationCreate):
    db_alloc = models.ServerAllocation(**allocation.dict())
    db.add(db_alloc)
    db.commit()
    db.refresh(db_alloc)
    return db_alloc


def get_allocations(db: Session, user_id: int):
    return db.query(models.ServerAllocation).filter(models.ServerAllocation.user_id == user_id).all()
