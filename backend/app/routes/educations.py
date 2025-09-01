from typing import List

from fastapi import APIRouter, HTTPException, Path

from .. import schemas

router = APIRouter()

_educations = [
    {"id": 1, "institution": "University", "degree": "BSc", "profile_id": None},
]


@router.get("/educations", response_model=List[schemas.EducationRead])
async def list_educations():
    return _educations


@router.post("/educations", response_model=schemas.EducationRead)
async def create_education(item: schemas.EducationCreate):
    next_id = max((e["id"] for e in _educations), default=0) + 1
    data = item.model_dump()
    data["id"] = next_id
    _educations.append(data)
    return data


@router.get("/educations/{education_id}", response_model=schemas.EducationRead)
async def get_education(education_id: int = Path(..., gt=0)):
    for e in _educations:
        if e["id"] == education_id:
            return e
    raise HTTPException(status_code=404, detail="Education not found")


@router.put("/educations/{education_id}", response_model=schemas.EducationRead)
async def update_education(education_id: int, item: schemas.EducationCreate):
    for idx, e in enumerate(_educations):
        if e["id"] == education_id:
            updated = e.copy()
            updated.update(item.model_dump(exclude_unset=True))
            updated["id"] = education_id
            _educations[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Education not found")


@router.delete("/educations/{education_id}")
async def delete_education(education_id: int):
    for idx, e in enumerate(_educations):
        if e["id"] == education_id:
            _educations.pop(idx)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Education not found")
