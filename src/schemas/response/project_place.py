from pydantic import BaseModel
from typing import Optional
from pydantic import ConfigDict

class ProjectPlaceOut(BaseModel):
    id: int
    external_id: int
    notes: Optional[str]
    visited: bool

    model_config = ConfigDict(from_attributes=True)