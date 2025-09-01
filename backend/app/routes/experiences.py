from typing import List

from fastapi import APIRouter, HTTPException, Path

from .. import schemas

router = APIRouter()

_experiences = [
    {
        "id": 1,
        "company": "Acme",
        "role": "Engineer",
        "skills": ["python"],
        "profile_id": None,
    },
]


@router.get("/experiences", response_model=List[schemas.ExperienceRead])
async def list_experiences():
    return _experiences


@router.post("/experiences", response_model=schemas.ExperienceRead)
async def create_experience(item: schemas.ExperienceCreate):
    next_id = max((e["id"] for e in _experiences), default=0) + 1
    data = item.model_dump()
    data["id"] = next_id
    _experiences.append(data)
    return data


@router.get("/experiences/{experience_id}", response_model=schemas.ExperienceRead)
async def get_experience(experience_id: int = Path(..., gt=0)):
    for e in _experiences:
        if e["id"] == experience_id:
            return e
    raise HTTPException(status_code=404, detail="Experience not found")


@router.put("/experiences/{experience_id}", response_model=schemas.ExperienceRead)
async def update_experience(experience_id: int, item: schemas.ExperienceCreate):
    for idx, e in enumerate(_experiences):
        if e["id"] == experience_id:
            updated = e.copy()
            updated.update(item.model_dump(exclude_unset=True))
            updated["id"] = experience_id
            _experiences[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Experience not found")


@router.delete("/experiences/{experience_id}")
async def delete_experience(experience_id: int):
    for idx, e in enumerate(_experiences):
        if e["id"] == experience_id:
            _experiences.pop(idx)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Experience not found")
