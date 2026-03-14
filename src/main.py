from fastapi import FastAPI
from src.routers import project_place, travel_project
app = FastAPI(
    title="Travel Planner API",
    version="1.0.0"
)
app.include_router(project_place.router)
app.include_router(travel_project.router)

@app.get("/")
async def root():
    return {"message": "Travel Planner API"}