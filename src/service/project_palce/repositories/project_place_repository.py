from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.project_place import ProjectPlace
from src.service.project_palce.interfaces.project_place_repository import ProjectPlaceRepository


class PlaceRepository(ProjectPlaceRepository):
    async def create(self, db: AsyncSession, place: ProjectPlace) -> ProjectPlace:
        db.add(place)
        await db.commit()
        await db.refresh(place)
        return place

    async def get(self, db: AsyncSession, place_id: int) -> Optional[ProjectPlace]:
        result = await db.execute(select(ProjectPlace).where(ProjectPlace.id == place_id))
        return result.scalar_one_or_none()

    async def list_by_project(self, db: AsyncSession, project_id: int) -> List[ProjectPlace]:
        result = await db.execute(select(ProjectPlace).where(ProjectPlace.project_id == project_id))
        return result.scalars().all()

    async def update(self, db: AsyncSession, place: ProjectPlace) -> ProjectPlace:
        await db.commit()
        await db.refresh(place)
        return place

    async def delete(self, db: AsyncSession, place: ProjectPlace) -> None:
        await db.delete(place)
        await db.commit()