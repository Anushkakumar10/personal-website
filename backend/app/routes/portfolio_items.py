from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from ..db import get_db
from ..logger import logger
from ..services import portfolio_items as portfolio_items_service

router = APIRouter()


@router.get(
    "/portfolio-items",
    response_model=List[schemas.PortfolioItemRead],
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def list_portfolio_items(
    profile_id: int = Query(None, gt=0), session: AsyncSession = Depends(get_db)
):
    return await portfolio_items_service.list_portfolio_items(profile_id, session)


@router.post(
    "/portfolio-items",
    response_model=schemas.PortfolioItemRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def create_portfolio_item(
    item: schemas.PortfolioItemCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    return await portfolio_items_service.create_portfolio_item(data, session)


@router.get(
    "/portfolio-items/{item_id}",
    response_model=schemas.PortfolioItemRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def get_portfolio_item(
    item_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await portfolio_items_service.get_portfolio_item(item_id, session)
    if not instance:
        logger.warning("Portfolio item %s not found", item_id)
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    return instance


@router.put(
    "/portfolio-items/{item_id}",
    response_model=schemas.PortfolioItemRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def update_portfolio_item(
    item_id: int,
    item: schemas.PortfolioItemCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    instance = await portfolio_items_service.update_portfolio_item(
        item_id, data, session
    )
    if not instance:
        logger.warning("Portfolio item %s not found for update", item_id)
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    return instance


@router.delete(
    "/portfolio-items/{item_id}",
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def delete_portfolio_item(item_id: int, session: AsyncSession = Depends(get_db)):
    ok = await portfolio_items_service.delete_portfolio_item(item_id, session)
    if not ok:
        logger.warning("Portfolio item %s not found for delete", item_id)
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    return {"ok": True}
