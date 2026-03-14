from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException
import httpx

from src.models.project_place import ProjectPlace
from src.schemas.request.project_place import ProjectPlaceCreate, PlaceUpdate
from src.service.project_palce.repositories.project_place_repository import PlaceRepository
from src.service.travel_project.repositories.travel_project_repository import ProjectRepository

MAX_PLACES = 10
ARTIC_API = "https://api.artic.edu/api/v1/artworks/"

class PlaceService:
    def __init__(self, place_repo: PlaceRepository, project_repo: ProjectRepository):
        self.place_repo = place_repo
        self.project_repo = project_repo

    async def add_place(self, db: AsyncSession, project_id: int, place_in: ProjectPlaceCreate) -> ProjectPlace:
        places = await self.place_repo.list_by_project(db, project_id)
        if len(places) >= MAX_PLACES:
            raise HTTPException(status_code=400, detail=f"Cannot add more than {MAX_PLACES} places")

        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{ARTIC_API}{place_in.external_id}")
            if resp.status_code != 200:
                raise HTTPException(status_code=400, detail=f"Place {place_in.external_id} does not exist in Art Institute API")

        if any(p.external_id == place_in.external_id for p in places):
            raise HTTPException(status_code=400, detail="Place already added to this project")

        place = ProjectPlace(
            project_id=project_id,
            external_id=place_in.external_id,
            notes=place_in.notes
        )
        place = await self.place_repo.create(db, place)
        await self._update_project_completed(db, project_id)
        return place

    async def update_place(self, db: AsyncSession, place_id: int, place_in: PlaceUpdate) -> ProjectPlace:
        place = await self.place_repo.get(db, place_id)
        if not place:
            raise HTTPException(status_code=404, detail="Place not found")
        if place_in.notes is not None:
            place.notes = place_in.notes
        if place_in.visited is not None:
            place.visited = place_in.visited
        place = await self.place_repo.update(db, place)
        await self._update_project_completed(db, place.project_id)
        return place

    async def list_places(self, db: AsyncSession, project_id: int) -> List[ProjectPlace]:
        return await self.place_repo.list_by_project(db, project_id)

    async def get_place(self, db: AsyncSession, place_id: int) -> ProjectPlace:
        place = await self.place_repo.get(db, place_id)
        if not place:
            raise HTTPException(status_code=404, detail="Place not found")
        return place

    async def _update_project_completed(self, db: AsyncSession, project_id: int):
        project = await self.project_repo.get(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        if project.places and all(p.visited for p in project.places):
            project.completed = True
        else:
            project.completed = False
        await self.project_repo.update(db, project)