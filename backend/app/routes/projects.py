from typing import Optional

from fastapi import APIRouter, Query

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


@router.get("/projects")
async def list_projects(skill: Optional[str] = Query(None)):
    if skill:
        return [p for p in _projects if skill in p.get("skills", [])]
    return _projects
