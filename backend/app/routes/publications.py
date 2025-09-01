from typing import List

from fastapi import APIRouter, HTTPException, Path

from .. import schemas

router = APIRouter()

_publications = [
    {"id": 1, "title": "Paper A", "publisher": "Journal", "profile_id": None},
]


@router.get("/publications", response_model=List[schemas.PublicationRead])
async def list_publications():
    return _publications


@router.post("/publications", response_model=schemas.PublicationRead)
async def create_publication(item: schemas.PublicationCreate):
    next_id = max((p["id"] for p in _publications), default=0) + 1
    data = item.model_dump()
    data["id"] = next_id
    _publications.append(data)
    return data


@router.get("/publications/{pub_id}", response_model=schemas.PublicationRead)
async def get_publication(pub_id: int = Path(..., gt=0)):
    for p in _publications:
        if p["id"] == pub_id:
            return p
    raise HTTPException(status_code=404, detail="Publication not found")


@router.put("/publications/{pub_id}", response_model=schemas.PublicationRead)
async def update_publication(pub_id: int, item: schemas.PublicationCreate):
    for idx, p in enumerate(_publications):
        if p["id"] == pub_id:
            updated = p.copy()
            updated.update(item.model_dump(exclude_unset=True))
            updated["id"] = pub_id
            _publications[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Publication not found")


@router.delete("/publications/{pub_id}")
async def delete_publication(pub_id: int):
    for idx, p in enumerate(_publications):
        if p["id"] == pub_id:
            _publications.pop(idx)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Publication not found")
