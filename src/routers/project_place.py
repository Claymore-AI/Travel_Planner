from fastapi import APIRouter, Depends

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from src.schemas.request.project_place import PlaceUpdate, ProjectPlaceCreate
from src.schemas.response.project_place import ProjectPlaceOut
from src.service.project_palce.repositories.project_place_repository import PlaceRepository
from src.service.project_palce.services.project_place_service import PlaceService
from src.service.travel_project.repositories.travel_project_repository import ProjectRepository

router = APIRouter(prefix="/projects/{project_id}/places", tags=["Places"])

# Dependency
def get_place_service() -> PlaceService:
    place_repo = PlaceRepository()
    project_repo = ProjectRepository()
    return PlaceService(place_repo=place_repo, project_repo=project_repo)


@router.post("/", response_model=ProjectPlaceOut)
async def add_place(
    project_id: int,
    place_in: ProjectPlaceCreate,
    db: AsyncSession = Depends(get_db),
    service: PlaceService = Depends(get_place_service)
):
    return await service.add_place(db, project_id, place_in)


@router.get("/", response_model=List[ProjectPlaceOut])
async def list_places(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    service: PlaceService = Depends(get_place_service)
):
    return await service.list_places(db, project_id)


@router.get("/{place_id}", response_model=ProjectPlaceOut)
async def get_place(
    project_id: int,
    place_id: int,
    db: AsyncSession = Depends(get_db),
    service: PlaceService = Depends(get_place_service)
):
    return await service.get_place(db, place_id)


@router.put("/{place_id}", response_model=ProjectPlaceOut)
async def update_place(
    project_id: int,
    place_id: int,
    place_in: PlaceUpdate,
    db: AsyncSession = Depends(get_db),
    service: PlaceService = Depends(get_place_service)
):
    return await service.update_place(db, place_id, place_in)