from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from ..auth import require_auth

router = APIRouter()

@router.post("/profile", response_model=schemas.Profile)
async def create_profile(
    profile: schemas.ProfileCreate,
    db: Session = Depends(get_db),
    _: str = Depends(require_auth)
):
    """Create a new profile (requires authentication)"""
    existing_profile = crud.get_profile(db)
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")
    return crud.create_profile(db, profile)

@router.get("/profile", response_model=schemas.Profile)
async def read_profile(db: Session = Depends(get_db)):
    """Get the profile"""
    profile = crud.get_profile(db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/profile", response_model=schemas.Profile)
async def update_profile(
    profile_update: schemas.ProfileUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(require_auth)
):
    """Update the profile (requires authentication)"""
    profile = crud.update_profile(db, profile_update)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
