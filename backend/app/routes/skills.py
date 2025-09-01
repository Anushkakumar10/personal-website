from typing import List, Optional

from fastapi import APIRouter, Query, HTTPException, Path

from .. import schemas

router = APIRouter()

_skills = [
    {"id": 1, "name": "python", "proficiency": 90, "years": 5.0, "profile_id": None},
    {"id": 2, "name": "fastapi", "proficiency": 80, "years": 2.0, "profile_id": None},
    {
        "id": 3,
        "name": "sqlalchemy",
        "proficiency": 75,
        "years": 3.0,
        "profile_id": None,
    },
    {
        "id": 4,
        "name": "javascript",
        "proficiency": 70,
        "years": 4.0,
        "profile_id": None,
    },
]


@router.get("/skills/top", response_model=List[schemas.SkillRead])
async def top_skills(limit: int = 10):
    return _skills[:limit]


@router.get("/skills/search", response_model=List[schemas.SkillRead])
async def search_skills(q: str = Query(...)):
    return [s for s in _skills if q.lower() in s["name"].lower()]


# New CRUD endpoints
@router.get("/skills", response_model=List[schemas.SkillRead])
async def list_skills():
    return _skills


@router.post("/skills", response_model=schemas.SkillRead)
async def create_skill(skill: schemas.SkillCreate):
    next_id = max((s["id"] for s in _skills), default=0) + 1
    item = skill.model_dump()
    item["id"] = next_id
    _skills.append(item)
    return item


@router.get("/skills/{skill_id}", response_model=schemas.SkillRead)
async def get_skill(skill_id: int = Path(..., gt=0)):
    for s in _skills:
        if s["id"] == skill_id:
            return s
    raise HTTPException(status_code=404, detail="Skill not found")


@router.put("/skills/{skill_id}", response_model=schemas.SkillRead)
async def update_skill(skill_id: int, skill: schemas.SkillCreate):
    for idx, s in enumerate(_skills):
        if s["id"] == skill_id:
            updated = s.copy()
            updated.update(skill.model_dump(exclude_unset=True))
            updated["id"] = skill_id
            _skills[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Skill not found")


@router.delete("/skills/{skill_id}")
async def delete_skill(skill_id: int):
    for idx, s in enumerate(_skills):
        if s["id"] == skill_id:
            _skills.pop(idx)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Skill not found")
