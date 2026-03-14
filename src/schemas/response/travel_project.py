from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from src.schemas.response.project_place import ProjectPlaceOut


class TravelProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_date: Optional[date]
    completed: bool
    places: List[ProjectPlaceOut] = []

    model_config = ConfigDict(from_attributes=True)