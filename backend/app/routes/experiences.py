from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db
from ..logger import logger

router = APIRouter()


@router.get("/experiences", response_model=List[schemas.ExperienceRead])
async def list_experiences(
    profile_id: int = Query(None, gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Listing experiences (profile_id=%s)", profile_id)
    filters = [models.Experience.profile_id == profile_id]
    return await models.Experience.list(filters=filters, session=session)


@router.post("/experiences", response_model=schemas.ExperienceRead)
async def create_experience(
    item: schemas.ExperienceCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    logger.info("Creating experience with data=%s", data)
    instance = await models.Experience.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    logger.info("Created experience id=%s", getattr(instance, "id", None))
    return instance


@router.get("/experiences/{experience_id}", response_model=schemas.ExperienceRead)
async def get_experience(
    experience_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Fetching experience id=%s", experience_id)
    instance = await models.Experience.get_by_id(experience_id, session=session)
    if not instance:
        logger.warning("Experience %s not found", experience_id)
        raise HTTPException(status_code=404, detail="Experience not found")
    return instance


@router.put("/experiences/{experience_id}", response_model=schemas.ExperienceRead)
async def update_experience(
    experience_id: int,
    item: schemas.ExperienceCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    logger.info("Updating experience id=%s data=%s", experience_id, data)
    instance = await models.Experience.update_by_id(
        experience_id, data, session=session
    )
    if not instance:
        logger.warning("Experience %s not found for update", experience_id)
        raise HTTPException(status_code=404, detail="Experience not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/experiences/{experience_id}")
async def delete_experience(
    experience_id: int, session: AsyncSession = Depends(get_db)
):
    logger.info("Deleting experience id=%s", experience_id)
    ok = await models.Experience.delete_by_id(experience_id, session=session)
    if not ok:
        logger.warning("Experience %s not found for delete", experience_id)
        raise HTTPException(status_code=404, detail="Experience not found")
    await session.commit()
    return {"ok": True}
