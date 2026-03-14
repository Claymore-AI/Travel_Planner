from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.travel_project import TravelProject
from src.service.travel_project.interfaces.travel_project_repository import TravelProjectRepository


def _query_with_places():
    return select(TravelProject).options(selectinload(TravelProject.places))


class ProjectRepository(TravelProjectRepository):
    async def create(self, db: AsyncSession, project: TravelProject) -> TravelProject:
        db.add(project)
        await db.commit()
        return await self.get(db, project.id)

    async def get(self, db: AsyncSession, project_id: int) -> Optional[TravelProject]:
        result = await db.execute(
            _query_with_places().where(TravelProject.id == project_id)
        )
        return result.scalar_one_or_none()

    async def list(self, db: AsyncSession) -> List[TravelProject]:
        result = await db.execute(_query_with_places())
        return result.scalars().all()

    async def update(self, db: AsyncSession, project: TravelProject) -> TravelProject:
        await db.commit()
        return await self.get(db, project.id)

    async def delete(self, db: AsyncSession, project: TravelProject) -> None:
        await db.delete(project)
        await db.commit()