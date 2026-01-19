-- Database schema for Me-API Playground
-- SQLite schema generated from SQLAlchemy models

-- Skills table
CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL UNIQUE
);

-- Projects table
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description TEXT NOT NULL,
    github_link VARCHAR,
    demo_link VARCHAR
);

-- Work table
CREATE TABLE work (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    duration VARCHAR NOT NULL,
    website_link VARCHAR
);

-- Profiles table
CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL UNIQUE,
    education VARCHAR NOT NULL,
    github_link VARCHAR,
    linkedin_link VARCHAR,
    portfolio_link VARCHAR
);

-- Association tables for many-to-many relationships
CREATE TABLE profile_skills (
    profile_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    PRIMARY KEY (profile_id, skill_id),
    FOREIGN KEY (profile_id) REFERENCES profiles (id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills (id) ON DELETE CASCADE
);

CREATE TABLE profile_projects (
    profile_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    PRIMARY KEY (profile_id, project_id),
    FOREIGN KEY (profile_id) REFERENCES profiles (id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

CREATE TABLE profile_work (
    profile_id INTEGER NOT NULL,
    work_id INTEGER NOT NULL,
    PRIMARY KEY (profile_id, work_id),
    FOREIGN KEY (profile_id) REFERENCES profiles (id) ON DELETE CASCADE,
    FOREIGN KEY (work_id) REFERENCES work (id) ON DELETE CASCADE
);

-- Indexes for better query performance
CREATE INDEX ix_skills_name ON skills (name);
CREATE INDEX ix_projects_title ON projects (title);
CREATE INDEX ix_work_company ON work (company);
CREATE INDEX ix_profiles_name ON profiles (name);
CREATE INDEX ix_profiles_email ON profiles (email);
