from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db
from ..logger import logger

router = APIRouter()


@router.get("/portfolio-items", response_model=List[schemas.PortfolioItemRead])
async def list_portfolio_items(
    profile_id: int = Query(None, gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Listing portfolio items (profile_id=%s)", profile_id)
    filters = [models.PortfolioItem.profile_id == profile_id]
    return await models.PortfolioItem.list(filters=filters or None, session=session)


@router.post("/portfolio-items", response_model=schemas.PortfolioItemRead)
async def create_portfolio_item(
    item: schemas.PortfolioItemCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    logger.info("Creating portfolio item with data=%s", data)
    instance = await models.PortfolioItem.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    logger.info("Created portfolio item id=%s", getattr(instance, "id", None))
    return instance


@router.get("/portfolio-items/{item_id}", response_model=schemas.PortfolioItemRead)
async def get_portfolio_item(
    item_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Fetching portfolio item id=%s", item_id)
    instance = await models.PortfolioItem.get_by_id(item_id, session=session)
    if not instance:
        logger.warning("Portfolio item %s not found", item_id)
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    return instance


@router.put("/portfolio-items/{item_id}", response_model=schemas.PortfolioItemRead)
async def update_portfolio_item(
    item_id: int,
    item: schemas.PortfolioItemCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    logger.info("Updating portfolio item id=%s data=%s", item_id, data)
    instance = await models.PortfolioItem.update_by_id(item_id, data, session=session)
    if not instance:
        logger.warning("Portfolio item %s not found for update", item_id)
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/portfolio-items/{item_id}")
async def delete_portfolio_item(item_id: int, session: AsyncSession = Depends(get_db)):
    logger.info("Deleting portfolio item id=%s", item_id)
    ok = await models.PortfolioItem.delete_by_id(item_id, session=session)
    if not ok:
        logger.warning("Portfolio item %s not found for delete", item_id)
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    await session.commit()
    return {"ok": True}
