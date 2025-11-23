from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils import decode_jwt
from database import SessionLocal
from models import Project
from schemas import ProjectCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_id(token: str):
    return decode_jwt(token)["user_id"]

@router.post("/create")
def create_project(data: ProjectCreate, token: str, db: Session = Depends(get_db)):
    uid = get_user_id(token)

    proj = Project(user_id=uid, name=data.name)
    db.add(proj)
    db.commit()
    return {"message": "created", "project_id": proj.id}

@router.get("")
def list_projects(token: str, db: Session = Depends(get_db)):
    uid = get_user_id(token)
    projects = db.query(Project).filter(Project.user_id == uid).all()
    return projects
