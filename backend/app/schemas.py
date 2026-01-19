from pydantic import BaseModel
from typing import List, Optional

class SkillBase(BaseModel):
    name: str

class Skill(SkillBase):
    id: int

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    title: str
    description: str
    github_link: Optional[str] = None
    demo_link: Optional[str] = None

class Project(ProjectBase):
    id: int

    class Config:
        from_attributes = True

class WorkBase(BaseModel):
    company: str
    role: str
    duration: str
    website_link: Optional[str] = None

class Work(WorkBase):
    id: int

    class Config:
        from_attributes = True

class ProfileBase(BaseModel):
    name: str
    email: str
    education: str
    github_link: Optional[str] = None
    linkedin_link: Optional[str] = None
    portfolio_link: Optional[str] = None

class ProfileCreate(ProfileBase):
    skills: List[str] = []
    projects: List[ProjectBase] = []
    work_experience: List[WorkBase] = []

class Profile(ProfileBase):
    id: int
    skills: List[Skill] = []
    projects: List[Project] = []
    work_experience: List[Work] = []

    class Config:
        from_attributes = True

class ProfileUpdate(ProfileBase):
    skills: Optional[List[str]] = None
    projects: Optional[List[ProjectBase]] = None
    work_experience: Optional[List[WorkBase]] = None

# Response models for queries
class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    github_link: Optional[str] = None
    demo_link: Optional[str] = None

class SkillCount(BaseModel):
    name: str
    count: int

class SearchResult(BaseModel):
    type: str  # "project", "skill", "work"
    title: str
    description: str
    relevance_score: float

class HealthResponse(BaseModel):
    status: str = "ok"
