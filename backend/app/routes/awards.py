from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from app.db import get_db
from app.logger import logger
from app.services import awards as awards_service

router = APIRouter()


@router.get(
    "/awards",
    response_model=List[schemas.AwardRead],
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def list_awards(
    session: AsyncSession = Depends(get_db),
    profile_id: int = Query(None, gt=0),
):
    return await awards_service.list_awards(profile_id, session)


@router.post(
    "/awards",
    response_model=schemas.AwardRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def create_award(
    item: schemas.AwardCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    return await awards_service.create_award(data, session)


@router.get(
    "/awards/{award_id}",
    response_model=schemas.AwardRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def get_award(
    award_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await awards_service.get_award(award_id, session)
    if not instance:
        logger.warning("Award %s not found", award_id)
        raise HTTPException(status_code=404, detail="Award not found")
    return instance


@router.put(
    "/awards/{award_id}",
    response_model=schemas.AwardRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def update_award(
    award_id: int, item: schemas.AwardCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump(exclude_unset=True)
    instance = await awards_service.update_award(award_id, data, session)
    if not instance:
        logger.warning("Award %s not found for update", award_id)
        raise HTTPException(status_code=404, detail="Award not found")
    return instance


@router.delete(
    "/awards/{award_id}",
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def delete_award(award_id: int, session: AsyncSession = Depends(get_db)):
    ok = await awards_service.delete_award(award_id, session)
    if not ok:
        logger.warning("Award %s not found for delete", award_id)
        raise HTTPException(status_code=404, detail="Award not found")
    return {"ok": True}
