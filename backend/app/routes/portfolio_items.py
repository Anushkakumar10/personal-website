from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db

router = APIRouter()


@router.get("/portfolio-items", response_model=List[schemas.PortfolioItemRead])
async def list_portfolio_items(session: AsyncSession = Depends(get_db)):
    return await models.PortfolioItem.list(session=session)


@router.post("/portfolio-items", response_model=schemas.PortfolioItemRead)
async def create_portfolio_item(
    item: schemas.PortfolioItemCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    instance = await models.PortfolioItem.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.get("/portfolio-items/{item_id}", response_model=schemas.PortfolioItemRead)
async def get_portfolio_item(
    item_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await models.PortfolioItem.get_by_id(item_id, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    return instance


@router.put("/portfolio-items/{item_id}", response_model=schemas.PortfolioItemRead)
async def update_portfolio_item(
    item_id: int,
    item: schemas.PortfolioItemCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    instance = await models.PortfolioItem.update_by_id(item_id, data, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/portfolio-items/{item_id}")
async def delete_portfolio_item(item_id: int, session: AsyncSession = Depends(get_db)):
    ok = await models.PortfolioItem.delete_by_id(item_id, session=session)
    if not ok:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    await session.commit()
    return {"ok": True}
