from typing import List

from fastapi import APIRouter, HTTPException, Path

from .. import schemas

router = APIRouter()

_awards = [
    {"id": 1, "title": "Award A", "issuer": "Org", "profile_id": None},
]


@router.get("/awards", response_model=List[schemas.AwardRead])
async def list_awards():
    return _awards


@router.post("/awards", response_model=schemas.AwardRead)
async def create_award(item: schemas.AwardCreate):
    next_id = max((a["id"] for a in _awards), default=0) + 1
    data = item.model_dump()
    data["id"] = next_id
    _awards.append(data)
    return data


@router.get("/awards/{award_id}", response_model=schemas.AwardRead)
async def get_award(award_id: int = Path(..., gt=0)):
    for a in _awards:
        if a["id"] == award_id:
            return a
    raise HTTPException(status_code=404, detail="Award not found")


@router.put("/awards/{award_id}", response_model=schemas.AwardRead)
async def update_award(award_id: int, item: schemas.AwardCreate):
    for idx, a in enumerate(_awards):
        if a["id"] == award_id:
            updated = a.copy()
            updated.update(item.model_dump(exclude_unset=True))
            updated["id"] = award_id
            _awards[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Award not found")


@router.delete("/awards/{award_id}")
async def delete_award(award_id: int):
    for idx, a in enumerate(_awards):
        if a["id"] == award_id:
            _awards.pop(idx)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Award not found")
