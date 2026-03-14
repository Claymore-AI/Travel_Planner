from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.project_place import ProjectPlace
from sqlalchemy.ext.asyncio import AsyncSession

class ProjectPlaceRepository(ABC):
    @abstractmethod
    async def create(self, db: AsyncSession, place: ProjectPlace) -> ProjectPlace:
        ...

    @abstractmethod
    async def get(self, db: AsyncSession, place_id: int) -> Optional[ProjectPlace]:
        ...

    @abstractmethod
    async def list_by_project(self, db: AsyncSession, project_id: int) -> List[ProjectPlace]:
        ...

    @abstractmethod
    async def update(self, db: AsyncSession, place: ProjectPlace) -> ProjectPlace:
        ...

    @abstractmethod
    async def delete(self, db: AsyncSession, place: ProjectPlace) -> None:
        ...