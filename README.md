# Travel Project API

A REST API for managing travel projects and places sourced from the Art Institute of Chicago collection.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Data Models](#data-models)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
  - [Projects](#projects)
  - [Places](#places)
- [Business Logic](#business-logic)
- [Error Codes](#error-codes)

---

## Tech Stack

- **Python 3.11+**
- **FastAPI** — web framework
- **SQLAlchemy** (async) — ORM
- **Pydantic v2** — schema validation
- **httpx** — async HTTP client for external requests
- **SQLite** — database
- **Art Institute of Chicago API** — external service for artwork validation

---

## Project Structure

```
src/
├── models/
│   ├── travel_project.py       # TravelProject ORM model
│   └── project_place.py        # ProjectPlace ORM model
├── schemas/
│   ├── request/
│   │   ├── travel_project.py   # TravelProjectCreate, ProjectUpdate
│   │   └── project_place.py    # ProjectPlaceCreate, PlaceUpdate
│   └── response/
│       ├── travel_project.py   # TravelProjectOut
│       └── project_place.py    # ProjectPlaceOut
├── service/
│   ├── travel_project/
│   │   ├── interfaces/
│   │   │   └── travel_project_repository.py  # ABC interface
│   │   ├── repositories/
│   │   │   └── travel_project_repository.py  # Repository implementation
│   │   └── services/
│   │       └── travel_project_services.py    # Business logic
│   └── project_palce/
│       ├── interfaces/
│       │   └── project_place_repository.py   # ABC interface
│       ├── repositories/
│       │   └── project_place_repository.py   # Repository implementation
│       └── services/
│           └── project_place_service.py      # Business logic
└── routers/
    ├── travel_project.py       # /projects routes
    └── project_place.py        # /projects/{id}/places routes
```

---

## Data Models

### TravelProject

| Field         | Type           | Description                                    |
|---------------|----------------|------------------------------------------------|
| `id`          | `int`          | Primary key                                    |
| `name`        | `str(255)`     | Project name (required)                        |
| `description` | `str \| None`  | Project description                            |
| `start_date`  | `date \| None` | Trip start date                                |
| `completed`   | `bool`         | Auto-managed completion flag (default `false`) |
| `places`      | `list[Place]`  | Related places (cascade delete)                |

### ProjectPlace

| Field         | Type          | Description                                      |
|---------------|---------------|--------------------------------------------------|
| `id`          | `int`         | Primary key                                      |
| `project_id`  | `int`         | FK → `travel_projects.id` (CASCADE)              |
| `external_id` | `str(255)`    | Artwork ID from the Art Institute of Chicago API |
| `notes`       | `str \| None` | Personal notes                                   |
| `visited`     | `bool`        | Whether the place was visited (default `false`)  |

> **Unique constraint:** `(project_id, external_id)` — the same place cannot be added twice to the same project.

---

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# create database
alembic upgrade head

# Start the server
uvicorn src.main:app --reload

# Interactive docs available at:
# http://localhost:8000/docs      ← Swagger UI
# http://localhost:8000/redoc     ← ReDoc
```

---

## API Reference

### Projects

Base URL: `/projects`

---

#### `POST /projects/` — Create a project

**Request body:**

```json
{
  "name": "Chicago Museum Tour",
  "description": "Visit the best artworks in the city",
  "start_date": "2025-06-15",
  "places": [
    { "external_id": 27992, "notes": "Main hall" },
    { "external_id": 111628 }
  ]
}
```

> `places` is optional. If provided, must contain between 1 and 10 items. Places are created together with the project in a single request.

**Response `201`:**

```json
{
  "id": 1,
  "name": "Chicago Museum Tour",
  "description": "Visit the best artworks in the city",
  "start_date": "2025-06-15",
  "completed": false,
  "places": [
    {
      "id": 1,
      "external_id": 27992,
      "notes": "Main hall",
      "visited": false
    },
    {
      "id": 2,
      "external_id": 111628,
      "notes": null,
      "visited": false
    }
  ]
}
```

**curl:**

```bash
curl -X POST http://localhost:8000/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Chicago Museum Tour",
    "description": "Visit the best artworks in the city",
    "start_date": "2025-06-15"
  }'
```

---

#### `GET /projects/` — List all projects

**Response `200`:**

```json
[
  {
    "id": 1,
    "name": "Chicago Museum Tour",
    "description": "Visit the best artworks in the city",
    "start_date": "2025-06-15",
    "completed": false,
    "places": []
  },
  {
    "id": 2,
    "name": "Paris Trip",
    "description": null,
    "start_date": null,
    "completed": true,
    "places": [...]
  }
]
```

**curl:**

```bash
curl http://localhost:8000/projects/
```

---

#### `GET /projects/{project_id}` — Get a project by ID

**URL parameters:**

| Parameter    | Type  | Description |
|--------------|-------|-------------|
| `project_id` | `int` | Project ID  |

**Response `200`:**

```json
{
  "id": 1,
  "name": "Chicago Museum Tour",
  "description": "Visit the best artworks in the city",
  "start_date": "2025-06-15",
  "completed": false,
  "places": [
    {
      "id": 1,
      "external_id": 27992,
      "notes": "Main hall",
      "visited": true
    }
  ]
}
```

**curl:**

```bash
curl http://localhost:8000/projects/1
```

---

#### `PUT /projects/{project_id}` — Update a project

All fields are optional — only include the ones you want to change.

**Request body:**

```json
{
  "name": "Updated Project Name",
  "start_date": "2025-09-01"
}
```

**Response `200`:**

```json
{
  "id": 1,
  "name": "Updated Project Name",
  "description": "Visit the best artworks in the city",
  "start_date": "2025-09-01",
  "completed": false,
  "places": [...]
}
```

**curl:**

```bash
curl -X PUT http://localhost:8000/projects/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Project Name", "start_date": "2025-09-01"}'
```

---

#### `DELETE /projects/{project_id}` — Delete a project

> ⚠️ **Cannot delete** a project if any of its places have `visited: true`.

**Response `204` No Content**

**curl:**

```bash
curl -X DELETE http://localhost:8000/projects/1
```

**Error `400` — project has visited places:**

```json
{
  "detail": "Cannot delete project with visited places"
}
```

---

### Places

Base URL: `/projects/{project_id}/places`

---

#### `POST /projects/{project_id}/places/` — Add a place

> Validates the `external_id` against the [Art Institute of Chicago API](https://api.artic.edu/docs/) before adding.

**URL parameters:**

| Parameter    | Type  | Description |
|--------------|-------|-------------|
| `project_id` | `int` | Project ID  |

**Request body:**

```json
{
  "external_id": 27993,
  "notes": "Impressionism hall, second floor"
}
```

**Response `200`:**

```json
{
  "id": 3,
  "external_id": 27993,
  "notes": "Impressionism hall, second floor",
  "visited": false
}
```

**curl:**

```bash
curl -X POST http://localhost:8000/projects/1/places/ \
  -H "Content-Type: application/json" \
  -d '{"external_id": 27993, "notes": "Impressionism hall, second floor"}'
```

**Possible errors:**

| Code  | Reason                                                |
|-------|-------------------------------------------------------|
| `400` | Project already has 10 places (maximum reached)       |
| `400` | `external_id` does not exist in the Art Institute API |
| `400` | This place has already been added to the project      |

```json
{ "detail": "Cannot add more than 10 places" }
{ "detail": "Place 99999 does not exist in Art Institute API" }
{ "detail": "Place already added to this project" }
```

---

#### `GET /projects/{project_id}/places/` — List places in a project

**Response `200`:**

```json
[
  {
    "id": 1,
    "external_id": 27993,
    "notes": "Impressionism hall",
    "visited": true
  },
  {
    "id": 2,
    "external_id": 111628,
    "notes": null,
    "visited": false
  }
]
```

**curl:**

```bash
curl http://localhost:8000/projects/1/places/
```

---

#### `GET /projects/{project_id}/places/{place_id}` — Get a place by ID

**URL parameters:**

| Parameter    | Type  | Description |
|--------------|-------|-------------|
| `project_id` | `int` | Project ID  |
| `place_id`   | `int` | Place ID    |

**Response `200`:**

```json
{
  "id": 1,
  "external_id": 27993,
  "notes": "Impressionism hall",
  "visited": true
}
```

**curl:**

```bash
curl http://localhost:8000/projects/1/places/1
```

---

#### `PUT /projects/{project_id}/places/{place_id}` — Update a place

Used to update notes or mark a place as visited.

**Request body:**

```json
{
  "notes": "Visited on Sunday — incredible collection",
  "visited": true
}
```

**Response `200`:**

```json
{
  "id": 1,
  "external_id": 27993,
  "notes": "Visited on Sunday — incredible collection",
  "visited": true
}
```

> When all places in a project have `visited: true`, the project's `completed` field is automatically set to `true`.

**curl:**

```bash
curl -X PUT http://localhost:8000/projects/1/places/1 \
  -H "Content-Type: application/json" \
  -d '{"visited": true, "notes": "Visited on Sunday — incredible collection"}'
```

---

## Business Logic

### Automatic project completion

The `completed` field on `TravelProject` is **never set manually**. It is recalculated automatically every time a place is added or updated:

- `completed = true` — if **all** places in the project have `visited: true` (and there is at least one)
- `completed = false` — in all other cases

### Places limit

Each project can hold a **maximum of 10 places**. Attempting to add an 11th place returns `400`.

### Place uniqueness

The same artwork (`external_id`) cannot be added to the same project twice. This is enforced both at the database level (UniqueConstraint on `project_id` + `external_id`) and in the service layer.

### External API validation

When adding a place, the service sends a request to `https://api.artic.edu/api/v1/artworks/{external_id}`. If the API returns anything other than `200`, the place is rejected.

### Deletion protection

A project **cannot be deleted** if any of its places have been marked as `visited: true`. This prevents accidental loss of travel history.

---

## Error Codes

| HTTP Code | Reason                                                   |
|-----------|----------------------------------------------------------|
| `400`     | Business rule violation (limit reached, duplicate, etc.) |
| `404`     | Resource not found (project or place)                    |
| `204`     | Successful deletion (no response body)                   |
| `422`     | Pydantic validation error (invalid request format)       |

---

## External Resources

- [Art Institute of Chicago API](https://api.artic.edu/docs/) — artwork database
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async Docs](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)