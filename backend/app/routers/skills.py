from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.get("/skills/top", response_model=List[schemas.SkillCount])
async def get_top_skills(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get top skills by usage count"""
    skills_data = crud.get_top_skills(db, limit)
    return [{"name": name, "count": count} for name, count in skills_data]
