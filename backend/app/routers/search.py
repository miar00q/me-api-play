from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.get("/search", response_model=List[schemas.SearchResult])
async def search_profiles(
    q: str = Query(..., description="Search query keyword"),
    db: Session = Depends(get_db)
):
    """Search across projects, skills, and work experience"""
    return crud.search_profiles(db, q)
