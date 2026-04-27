from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.project import ProjectResponse, ProjectCU
from typing import Annotated
from services.project_service import create_project, delete_project, read_all_project, read_project, update_project
from api.deps import verify_internal_api_key
from uuid import UUID

router = APIRouter()

@router.post("/create", response_model=ProjectResponse, status_code=201)
def create_route(
      _: Annotated[None, Depends(verify_internal_api_key)],
  payload: Annotated[ProjectCU, Body(...)],
  db: Session = Depends(get_db)
):
    return create_project(db, payload)

@router.get("/read/{project_id}",response_model=ProjectResponse, status_code=201)
def read_route(
    _: Annotated[None, Depends(verify_internal_api_key)],
    project_id: UUID,
    db: Session = Depends(get_db)
):
    return read_project(db, project_id)

@router.get("/read/all/{user_id}", response_model=ProjectResponse, status_code=201)
def read_all_route(
    _: Annotated[None, Depends(verify_internal_api_key)],
    user_id: UUID,
    db: Session = Depends(get_db)
):
    return read_all_project(db, user_id)  

@router.put("/update/{project_id}", response_model=ProjectResponse, status_code=201)
def update_route(
    _: Annotated[None, Depends(verify_internal_api_key)],
    payload: Annotated[ProjectCU, Body(...)],
    project_id: UUID,
    db: Session = Depends(get_db)
):
    return update_project(db, payload)

@router.delete("/delete/{project_id}", response_model=ProjectResponse, status_code=201)
def delete_route(
    project_id: UUID,
     _: Annotated[None, Depends(verify_internal_api_key)],
    db: Session = Depends(get_db),
):
    return delete_project(db, project_id)  
