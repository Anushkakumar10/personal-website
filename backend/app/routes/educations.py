from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db
from ..logger import logger

router = APIRouter()


@router.get("/educations", response_model=List[schemas.EducationRead])
async def list_educations(
    profile_id: int = Query(None, gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Listing educations (profile_id=%s)", profile_id)
    filters = [models.Education.profile_id == profile_id]
    return await models.Education.list(filters=filters, session=session)


@router.post("/educations", response_model=schemas.EducationRead)
async def create_education(
    item: schemas.EducationCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    logger.info("Creating education with data=%s", data)
    instance = await models.Education.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    logger.info("Created education id=%s", getattr(instance, "id", None))
    return instance


@router.get("/educations/{education_id}", response_model=schemas.EducationRead)
async def get_education(
    education_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Fetching education id=%s", education_id)
    instance = await models.Education.get_by_id(education_id, session=session)
    if not instance:
        logger.warning("Education %s not found", education_id)
        raise HTTPException(status_code=404, detail="Education not found")
    return instance


@router.put("/educations/{education_id}", response_model=schemas.EducationRead)
async def update_education(
    education_id: int,
    item: schemas.EducationCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    logger.info("Updating education id=%s data=%s", education_id, data)
    instance = await models.Education.update_by_id(education_id, data, session=session)
    if not instance:
        logger.warning("Education %s not found for update", education_id)
        raise HTTPException(status_code=404, detail="Education not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/educations/{education_id}")
async def delete_education(education_id: int, session: AsyncSession = Depends(get_db)):
    logger.info("Deleting education id=%s", education_id)
    ok = await models.Education.delete_by_id(education_id, session=session)
    if not ok:
        logger.warning("Education %s not found for delete", education_id)
        raise HTTPException(status_code=404, detail="Education not found")
    await session.commit()
    return {"ok": True}
