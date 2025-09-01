from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db
from ..logger import logger

router = APIRouter()


@router.get("/awards", response_model=List[schemas.AwardRead])
async def list_awards(
    session: AsyncSession = Depends(get_db),
    profile_id: int = Query(None, gt=0),
):
    logger.info("Listing awards (profile_id=%s)", profile_id)
    filters = [models.Award.profile_id == profile_id]
    return await models.Award.list(filters=filters, session=session)


@router.post("/awards", response_model=schemas.AwardRead)
async def create_award(
    item: schemas.AwardCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    logger.info("Creating award with data=%s", data)
    instance = await models.Award.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    logger.info("Created award id=%s", getattr(instance, "id", None))
    return instance


@router.get("/awards/{award_id}", response_model=schemas.AwardRead)
async def get_award(
    award_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Fetching award id=%s", award_id)
    instance = await models.Award.get_by_id(award_id, session=session)
    if not instance:
        logger.warning("Award %s not found", award_id)
        raise HTTPException(status_code=404, detail="Award not found")
    return instance


@router.put("/awards/{award_id}", response_model=schemas.AwardRead)
async def update_award(
    award_id: int, item: schemas.AwardCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump(exclude_unset=True)
    logger.info("Updating award id=%s data=%s", award_id, data)
    instance = await models.Award.update_by_id(award_id, data, session=session)
    if not instance:
        logger.warning("Award %s not found for update", award_id)
        raise HTTPException(status_code=404, detail="Award not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/awards/{award_id}")
async def delete_award(award_id: int, session: AsyncSession = Depends(get_db)):
    logger.info("Deleting award id=%s", award_id)
    ok = await models.Award.delete_by_id(award_id, session=session)
    if not ok:
        logger.warning("Award %s not found for delete", award_id)
        raise HTTPException(status_code=404, detail="Award not found")
    await session.commit()
    return {"ok": True}
