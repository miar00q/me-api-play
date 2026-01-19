from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import os

def seed_database():
    # Create tables
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if profile already exists
        existing_profile = crud.get_profile(db)
        if existing_profile:
            print("Database already seeded")
            return

        # Create profile data
        profile_data = schemas.ProfileCreate(
            name="Mir Asrar",
            email="mir.asrar@example.com",  # Using placeholder as requested
            education="NIT Delhi – Electronics & Communication Engineering",
            github_link="https://github.com/mirasrar",
            linkedin_link="https://linkedin.com/in/mirasrar",
            portfolio_link="https://mirasrar.dev",
            skills=[
                "Python", "FastAPI", "SQL", "MongoDB", "MATLAB", "C", "Java",
                "Web Development", "ANSYS HFSS"
            ],
            projects=[
                schemas.ProjectBase(
                    title="Solar Powered Wireless Charger",
                    description="Designed and implemented a solar-powered wireless charging system for mobile devices",
                    github_link="https://github.com/mirasrar/solar-charger",
                    demo_link="https://demo.mirasrar.dev/solar-charger"
                ),
                schemas.ProjectBase(
                    title="Auto Cut-off Battery Charger",
                    description="Developed an intelligent battery charger with automatic cut-off functionality",
                    github_link="https://github.com/mirasrar/auto-charger",
                    demo_link="https://demo.mirasrar.dev/auto-charger"
                ),
                schemas.ProjectBase(
                    title="Arduino Qibla Compass",
                    description="Created a Qibla direction finder using Arduino and GPS module",
                    github_link="https://github.com/mirasrar/qibla-compass",
                    demo_link="https://demo.mirasrar.dev/qibla-compass"
                ),
                schemas.ProjectBase(
                    title="Audio Reactive LED Strip",
                    description="Built an LED strip that reacts to audio input with real-time visualization",
                    github_link="https://github.com/mirasrar/audio-led",
                    demo_link="https://demo.mirasrar.dev/audio-led"
                )
            ],
            work_experience=[
                # Add work experience if available, using placeholders for now
            ]
        )

        # Create profile
        profile = crud.create_profile(db, profile_data)
        print(f"Database seeded successfully with profile for {profile.name}")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
