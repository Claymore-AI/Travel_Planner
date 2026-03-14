from datetime import date
from typing import Optional
from pydantic import BaseModel, conlist

from src.schemas.request.project_place import ProjectPlaceCreate


class TravelProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    places: Optional[conlist(ProjectPlaceCreate, min_length=1, max_length=10)] = []

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None