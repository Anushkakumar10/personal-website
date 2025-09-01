from typing import List

from fastapi import APIRouter, HTTPException, Path

from .. import schemas

router = APIRouter()

_references = [
    {
        "id": 1,
        "name": "Ref A",
        "relation": "Manager",
        "contact_info": "ref@example.com",
        "profile_id": None,
    },
]


@router.get("/references", response_model=List[schemas.ReferenceRead])
async def list_references():
    return _references


@router.post("/references", response_model=schemas.ReferenceRead)
async def create_reference(item: schemas.ReferenceCreate):
    next_id = max((r["id"] for r in _references), default=0) + 1
    data = item.model_dump()
    data["id"] = next_id
    _references.append(data)
    return data


@router.get("/references/{ref_id}", response_model=schemas.ReferenceRead)
async def get_reference(ref_id: int = Path(..., gt=0)):
    for r in _references:
        if r["id"] == ref_id:
            return r
    raise HTTPException(status_code=404, detail="Reference not found")


@router.put("/references/{ref_id}", response_model=schemas.ReferenceRead)
async def update_reference(ref_id: int, item: schemas.ReferenceCreate):
    for idx, r in enumerate(_references):
        if r["id"] == ref_id:
            updated = r.copy()
            updated.update(item.model_dump(exclude_unset=True))
            updated["id"] = ref_id
            _references[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Reference not found")


@router.delete("/references/{ref_id}")
async def delete_reference(ref_id: int):
    for idx, r in enumerate(_references):
        if r["id"] == ref_id:
            _references.pop(idx)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Reference not found")
