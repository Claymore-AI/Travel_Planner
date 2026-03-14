from fastapi import APIRouter, Depends

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from src.schemas.request.travel_project import ProjectUpdate, TravelProjectCreate
from src.schemas.response.travel_project import TravelProjectOut
from src.service.project_palce.repositories.project_place_repository import PlaceRepository
from src.service.project_palce.services.project_place_service import PlaceService
from src.service.travel_project.repositories.travel_project_repository import ProjectRepository
from src.service.travel_project.services.travel_project_services import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_service() -> ProjectService:
    project_repo = ProjectRepository()
    place_repo = PlaceRepository()
    place_service = PlaceService(place_repo=place_repo, project_repo=project_repo)
    return ProjectService(project_repo=project_repo, place_service=place_service)


@router.post("/", response_model=TravelProjectOut)
async def create_project(
    project_in: TravelProjectCreate,
    db: AsyncSession = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    return await service.create_project(db, project_in)


@router.get("/", response_model=List[TravelProjectOut])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    return await service.list_projects(db)


@router.get("/{project_id}", response_model=TravelProjectOut)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    return await service.get_project(db, project_id)


@router.put("/{project_id}", response_model=TravelProjectOut)
async def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    return await service.update_project(db, project_id, project_in)


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    await service.delete_project(db, project_id)
    return None