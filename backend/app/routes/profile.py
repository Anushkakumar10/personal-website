from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from ..db import get_db
from ..logger import logger
from ..services import profile as profile_service

router = APIRouter()


@router.get(
    "/profiles/{profile_id}",
    response_model=schemas.ProfileRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def get_profile(
    profile_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Fetching profile id=%s", profile_id)
    profile = await profile_service.get_profile(profile_id, session)
    if not profile:
        logger.warning("Profile id=%s not found", profile_id)
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put(
    "/profiles/{profile_id}",
    response_model=schemas.ProfileRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def update_profile(
    profile: schemas.ProfileCreate,
    profile_id: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_db),
):
    data = profile.model_dump(exclude_unset=True)
    logger.info("Updating profile id=%s with data=%s", profile_id, data)
    profile_obj = await profile_service.update_profile(profile_id, data, session)
    if not profile_obj:
        logger.warning("Profile id=%s not found for update", profile_id)
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile_obj
