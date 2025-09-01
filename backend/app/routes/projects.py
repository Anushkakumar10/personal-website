from typing import Optional, List

from fastapi import APIRouter, Query, HTTPException, Path

from .. import schemas

router = APIRouter()

_projects = [
    {
        "id": 1,
        "title": "Project A",
        "description": "A Python project",
        "skills": ["python"],
    },
    {
        "id": 2,
        "title": "Project B",
        "description": "A JS project",
        "skills": ["javascript"],
    },
]


@router.get("/projects", response_model=List[schemas.ProjectRead])
async def list_projects(skill: Optional[str] = Query(None)):
    if skill:
        return [p for p in _projects if skill in p.get("skills", [])]
    return _projects


@router.post("/projects", response_model=schemas.ProjectRead)
async def create_project(project: schemas.ProjectCreate):
    next_id = max((p["id"] for p in _projects), default=0) + 1
    item = project.model_dump()
    item["id"] = next_id
    _projects.append(item)
    return item


@router.get("/projects/{project_id}", response_model=schemas.ProjectRead)
async def get_project(project_id: int = Path(..., gt=0)):
    for p in _projects:
        if p["id"] == project_id:
            return p
    raise HTTPException(status_code=404, detail="Project not found")


@router.put("/projects/{project_id}", response_model=schemas.ProjectRead)
async def update_project(project_id: int, project: schemas.ProjectCreate):
    for idx, p in enumerate(_projects):
        if p["id"] == project_id:
            updated = p.copy()
            updated.update(project.model_dump(exclude_unset=True))
            updated["id"] = project_id
            _projects[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Project not found")


@router.delete("/projects/{project_id}")
async def delete_project(project_id: int):
    for idx, p in enumerate(_projects):
        if p["id"] == project_id:
            _projects.pop(idx)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Project not found")
