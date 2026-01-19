from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import health, profile, projects, skills, search
from .database import engine
from . import models
from .seed import seed_database

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Seed database on startup
seed_database()

app = FastAPI(
    title="Me-API Playground",
    description="A REST API for managing personal profile data",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(profile.router)
app.include_router(projects.router)
app.include_router(skills.router)
app.include_router(search.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Me-API Playground"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
