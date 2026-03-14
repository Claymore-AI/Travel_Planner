from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.travel_project import TravelProject
from sqlalchemy.ext.asyncio import AsyncSession

class TravelProjectRepository(ABC):
    @abstractmethod
    async def create(self, db: AsyncSession, project: TravelProject) -> TravelProject:
        ...

    @abstractmethod
    async def get(self, db: AsyncSession, project_id: int) -> Optional[TravelProject]:
        ...

    @abstractmethod
    async def list(self, db: AsyncSession) -> List[TravelProject]:
        ...

    @abstractmethod
    async def update(self, db: AsyncSession, project: TravelProject) -> TravelProject:
        ...

    @abstractmethod
    async def delete(self, db: AsyncSession, project: TravelProject) -> None:
        ...