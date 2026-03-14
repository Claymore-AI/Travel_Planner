from pydantic import BaseModel
from typing import Optional

class ProjectPlaceCreate(BaseModel):
    external_id: int
    notes: Optional[str] = None

class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    visited: Optional[bool] = None