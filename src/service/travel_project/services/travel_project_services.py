from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from src.models.travel_project import TravelProject
from src.schemas.request.travel_project import ProjectUpdate, TravelProjectCreate
from src.service.travel_project.repositories.travel_project_repository import ProjectRepository


class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo

    async def create_project(self, db: AsyncSession, project_in: TravelProjectCreate) -> TravelProject:
        project = TravelProject(
            name=project_in.name,
            description=project_in.description,
            start_date=project_in.start_date
        )
        return await self.project_repo.create(db, project)

    async def get_project(self, db: AsyncSession, project_id: int) -> TravelProject:
        project = await self.project_repo.get(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

    async def list_projects(self, db: AsyncSession) -> List[TravelProject]:
        return await self.project_repo.list(db)

    async def update_project(self, db: AsyncSession, project_id: int, project_in: ProjectUpdate) -> TravelProject:
        project = await self.get_project(db, project_id)
        if project_in.name is not None:
            project.name = project_in.name
        if project_in.description is not None:
            project.description = project_in.description
        if project_in.start_date is not None:
            project.start_date = project_in.start_date
        return await self.project_repo.update(db, project)

    async def delete_project(self, db: AsyncSession, project_id: int):
        project = await self.get_project(db, project_id)
        if any(p.visited for p in project.places):
            raise HTTPException(status_code=400, detail="Cannot delete project with visited places")
        await self.project_repo.delete(db, project)