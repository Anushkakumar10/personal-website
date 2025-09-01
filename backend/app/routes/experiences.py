from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from app.db import get_db
from app.logger import logger
from app.services import experiences as experiences_service

router = APIRouter()


@router.get(
    "/experiences",
    response_model=List[schemas.ExperienceRead],
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def list_experiences(
    profile_id: int = Query(None, gt=0), session: AsyncSession = Depends(get_db)
):
    return await experiences_service.list_experiences(profile_id, session)


@router.post(
    "/experiences",
    response_model=schemas.ExperienceRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def create_experience(
    item: schemas.ExperienceCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    return await experiences_service.create_experience(data, session)


@router.get(
    "/experiences/{experience_id}",
    response_model=schemas.ExperienceRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def get_experience(
    experience_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await experiences_service.get_experience(experience_id, session)
    if not instance:
        logger.warning("Experience %s not found", experience_id)
        raise HTTPException(status_code=404, detail="Experience not found")
    return instance


@router.put(
    "/experiences/{experience_id}",
    response_model=schemas.ExperienceRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def update_experience(
    experience_id: int,
    item: schemas.ExperienceCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    instance = await experiences_service.update_experience(experience_id, data, session)
    if not instance:
        logger.warning("Experience %s not found for update", experience_id)
        raise HTTPException(status_code=404, detail="Experience not found")
    return instance


@router.delete(
    "/experiences/{experience_id}",
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def delete_experience(
    experience_id: int, session: AsyncSession = Depends(get_db)
):
    ok = await experiences_service.delete_experience(experience_id, session)
    if not ok:
        logger.warning("Experience %s not found for delete", experience_id)
        raise HTTPException(status_code=404, detail="Experience not found")
    return {"ok": True}
