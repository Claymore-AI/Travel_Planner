from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.travel_project import TravelProject
from src.service.travel_project.interfaces.travel_project_repository import TravelProjectRepository


class ProjectRepository(TravelProjectRepository):
    async def create(self, db: AsyncSession, project: TravelProject) -> TravelProject:
        db.add(project)
        await db.commit()
        await db.refresh(project)
        return project

    async def get(self, db: AsyncSession, project_id: int) -> Optional[TravelProject]:
        result = await db.execute(select(TravelProject).where(TravelProject.id == project_id))
        return result.scalar_one_or_none()

    async def list(self, db: AsyncSession) -> List[TravelProject]:
        result = await db.execute(select(TravelProject))
        return result.scalars().all()

    async def update(self, db: AsyncSession, project: TravelProject) -> TravelProject:
        await db.commit()
        await db.refresh(project)
        return project

    async def delete(self, db: AsyncSession, project: TravelProject) -> None:
        await db.delete(project)
        await db.commit()