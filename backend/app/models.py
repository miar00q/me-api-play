from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Table

# Association tables for many-to-many relationships
profile_skills = Table(
    'profile_skills',
    Base.metadata,
    Column('profile_id', Integer, ForeignKey('profiles.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)

profile_projects = Table(
    'profile_projects',
    Base.metadata,
    Column('profile_id', Integer, ForeignKey('profiles.id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True)
)

profile_work = Table(
    'profile_work',
    Base.metadata,
    Column('profile_id', Integer, ForeignKey('profiles.id'), primary_key=True),
    Column('work_id', Integer, ForeignKey('work.id'), primary_key=True)
)

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    github_link = Column(String, nullable=True)
    demo_link = Column(String, nullable=True)

class Work(Base):
    __tablename__ = "work"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True)
    role = Column(String)
    duration = Column(String)
    website_link = Column(String, nullable=True)

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    education = Column(String)

    # Links
    github_link = Column(String, nullable=True)
    linkedin_link = Column(String, nullable=True)
    portfolio_link = Column(String, nullable=True)

    # Relationships
    skills = relationship("Skill", secondary=profile_skills, backref="profiles")
    projects = relationship("Project", secondary=profile_projects, backref="profiles")
    work_experience = relationship("Work", secondary=profile_work, backref="profiles")
