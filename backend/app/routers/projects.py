from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.get("/projects", response_model=List[schemas.ProjectResponse])
async def get_projects_by_skill(
    skill: str = Query(..., description="Skill to filter projects by"),
    db: Session = Depends(get_db)
):
    """Get projects filtered by skill"""
    return crud.get_projects_by_skill(db, skill)
