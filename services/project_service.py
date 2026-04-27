from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID

from models.project import Project
from schemas.project import ProjectCU

def create_project(db: Session, payload: ProjectCU)-> Project:
    record = Project(user_id = payload.user_id,
                    name = payload.name, 
                    description = payload.description,
                    due_date = payload.due_date,
                    min_session_time = payload.min_session_time)
    db.add(record)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code= 409,
            detail="user not found"
        ) from exc
    db.refresh(record)
    return record
    
def delete_project(db: Session, project_id: UUID) -> str:
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(project)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Delete failed"
        ) from exc

    return "Delete successful!"
def read_project(db: Session, project_id:UUID)-> Project:
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()
    if(not project):
        raise HTTPException(
            status_code=404,
            detail="Project not found!"
        )
    return project

def read_all_project(db: Session, user_id: UUID)-> Project:
    project = db.query(Project).filter(
        Project.user_id == user_id
    ).get()
    if(not project):
        raise HTTPException(
            status_code=404,
            detail="User has no project!"
        )
    return project

def update_project(db: Session,project_id: UUID,  payload: ProjectCU)-> Project:
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if(not project):
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    
    project.user_id = payload.user_id
    project.name= payload.name
    project.description = payload.description
    project.due_date = payload.due_date
    project.min_session_time = payload.min_session_time

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Update failed!"
        )
    db.refresh(project)
    return project