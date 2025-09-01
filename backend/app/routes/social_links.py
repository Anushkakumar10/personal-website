from typing import List

from fastapi import APIRouter, HTTPException, Path

from .. import schemas

router = APIRouter()

_social_links = [
    {
        "id": 1,
        "platform": "github",
        "url": "https://github.com/me",
        "username": "me",
        "profile_id": None,
    },
]


@router.get("/social-links", response_model=List[schemas.SocialLinkRead])
async def list_social_links():
    return _social_links


@router.post("/social-links", response_model=schemas.SocialLinkRead)
async def create_social_link(item: schemas.SocialLinkCreate):
    next_id = max((s["id"] for s in _social_links), default=0) + 1
    data = item.model_dump()
    data["id"] = next_id
    _social_links.append(data)
    return data


@router.get("/social-links/{link_id}", response_model=schemas.SocialLinkRead)
async def get_social_link(link_id: int = Path(..., gt=0)):
    for s in _social_links:
        if s["id"] == link_id:
            return s
    raise HTTPException(status_code=404, detail="Social link not found")


@router.put("/social-links/{link_id}", response_model=schemas.SocialLinkRead)
async def update_social_link(link_id: int, item: schemas.SocialLinkCreate):
    for idx, s in enumerate(_social_links):
        if s["id"] == link_id:
            updated = s.copy()
            updated.update(item.model_dump(exclude_unset=True))
            updated["id"] = link_id
            _social_links[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Social link not found")


@router.delete("/social-links/{link_id}")
async def delete_social_link(link_id: int):
    for idx, s in enumerate(_social_links):
        if s["id"] == link_id:
            _social_links.pop(idx)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Social link not found")
