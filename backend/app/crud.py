from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from . import models, schemas
from typing import List, Optional

def get_profile(db: Session) -> Optional[models.Profile]:
    return db.query(models.Profile).first()

def create_profile(db: Session, profile: schemas.ProfileCreate) -> models.Profile:
    # Create skills
    skill_objects = []
    for skill_name in profile.skills:
        skill = db.query(models.Skill).filter(models.Skill.name == skill_name).first()
        if not skill:
            skill = models.Skill(name=skill_name)
            db.add(skill)
        skill_objects.append(skill)

    # Create projects
    project_objects = []
    for project_data in profile.projects:
        project = models.Project(**project_data.dict())
        db.add(project)
        project_objects.append(project)

    # Create work experience
    work_objects = []
    for work_data in profile.work_experience:
        work = models.Work(**work_data.dict())
        db.add(work)
        work_objects.append(work)

    # Create profile
    db_profile = models.Profile(
        name=profile.name,
        email=profile.email,
        education=profile.education,
        github_link=profile.github_link,
        linkedin_link=profile.linkedin_link,
        portfolio_link=profile.portfolio_link,
        skills=skill_objects,
        projects=project_objects,
        work_experience=work_objects
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, profile_update: schemas.ProfileUpdate) -> Optional[models.Profile]:
    profile = get_profile(db)
    if not profile:
        return None

    # Update basic fields
    update_data = profile_update.dict(exclude_unset=True)
    skills = update_data.pop('skills', None)
    projects = update_data.pop('projects', None)
    work_experience = update_data.pop('work_experience', None)

    for field, value in update_data.items():
        setattr(profile, field, value)

    # Update skills if provided
    if skills is not None:
        profile.skills.clear()
        for skill_name in skills:
            skill = db.query(models.Skill).filter(models.Skill.name == skill_name).first()
            if not skill:
                skill = models.Skill(name=skill_name)
                db.add(skill)
            profile.skills.append(skill)

    # Update projects if provided
    if projects is not None:
        profile.projects.clear()
        for project_data in projects:
            project = models.Project(**project_data)
            db.add(project)
            profile.projects.append(project)

    # Update work experience if provided
    if work_experience is not None:
        profile.work_experience.clear()
        for work_data in work_experience:
            work = models.Work(**work_data)
            db.add(work)
            profile.work_experience.append(work)

    db.commit()
    db.refresh(profile)
    return profile

def get_projects_by_skill(db: Session, skill: str) -> List[models.Project]:
    return db.query(models.Project).join(models.Profile.projects).join(models.Profile.skills).filter(models.Skill.name.ilike(f"%{skill}%")).all()

def get_top_skills(db: Session, limit: int = 10) -> List[dict]:
    return db.query(
        models.Skill.name,
        func.count(models.profile_skills.c.profile_id).label('count')
    ).join(models.profile_skills).group_by(models.Skill.id).order_by(func.count(models.profile_skills.c.profile_id).desc()).limit(limit).all()

def search_profiles(db: Session, query: str) -> List[dict]:
    results = []

    # Search in projects
    projects = db.query(models.Project).filter(
        or_(
            models.Project.title.ilike(f"%{query}%"),
            models.Project.description.ilike(f"%{query}%")
        )
    ).all()

    for project in projects:
        results.append({
            "type": "project",
            "title": project.title,
            "description": project.description,
            "relevance_score": 1.0
        })

    # Search in skills
    skills = db.query(models.Skill).filter(models.Skill.name.ilike(f"%{query}%")).all()

    for skill in skills:
        results.append({
            "type": "skill",
            "title": skill.name,
            "description": f"Technical skill: {skill.name}",
            "relevance_score": 0.8
        })

    # Search in work experience
    work = db.query(models.Work).filter(
        or_(
            models.Work.company.ilike(f"%{query}%"),
            models.Work.role.ilike(f"%{query}%")
        )
    ).all()

    for w in work:
        results.append({
            "type": "work",
            "title": f"{w.role} at {w.company}",
            "description": f"Duration: {w.duration}",
            "relevance_score": 0.7
        })

    return results
