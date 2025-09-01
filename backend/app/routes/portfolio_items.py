from typing import List

from fastapi import APIRouter, HTTPException, Path

from .. import schemas

router = APIRouter()

_portfolio_items = [
    {
        "id": 1,
        "title": "Portfolio A",
        "description": "Demo",
        "skills": [],
        "profile_id": None,
    },
]


@router.get("/portfolio-items", response_model=List[schemas.PortfolioItemRead])
async def list_portfolio_items():
    return _portfolio_items


@router.post("/portfolio-items", response_model=schemas.PortfolioItemRead)
async def create_portfolio_item(item: schemas.PortfolioItemCreate):
    next_id = max((p["id"] for p in _portfolio_items), default=0) + 1
    data = item.model_dump()
    data["id"] = next_id
    _portfolio_items.append(data)
    return data


@router.get("/portfolio-items/{item_id}", response_model=schemas.PortfolioItemRead)
async def get_portfolio_item(item_id: int = Path(..., gt=0)):
    for p in _portfolio_items:
        if p["id"] == item_id:
            return p
    raise HTTPException(status_code=404, detail="Portfolio item not found")


@router.put("/portfolio-items/{item_id}", response_model=schemas.PortfolioItemRead)
async def update_portfolio_item(item_id: int, item: schemas.PortfolioItemCreate):
    for idx, p in enumerate(_portfolio_items):
        if p["id"] == item_id:
            updated = p.copy()
            updated.update(item.model_dump(exclude_unset=True))
            updated["id"] = item_id
            _portfolio_items[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Portfolio item not found")


@router.delete("/portfolio-items/{item_id}")
async def delete_portfolio_item(item_id: int):
    for idx, p in enumerate(_portfolio_items):
        if p["id"] == item_id:
            _portfolio_items.pop(idx)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Portfolio item not found")
