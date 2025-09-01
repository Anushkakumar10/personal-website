from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from app.db import get_db
from app.logger import logger
from app.services import educations as educations_service

router = APIRouter()


@router.get(
    "/educations",
    response_model=List[schemas.EducationRead],
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def list_educations(
    profile_id: int = Query(None, gt=0),
    page: int = Query(1, gt=0),
    per_page: int = Query(20, gt=1, le=100),
    session: AsyncSession = Depends(get_db),
):
    return await educations_service.list_educations(
        profile_id, page=page, per_page=per_page, session=session
    )


@router.post(
    "/educations",
    response_model=schemas.EducationRead,
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def create_education(
    item: schemas.EducationCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    return await educations_service.create_education(data, session)


@router.get(
    "/educations/{education_id}",
    response_model=schemas.EducationRead,
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def get_education(
    education_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await educations_service.get_education(education_id, session)
    if not instance:
        logger.warning("Education %s not found", education_id)
        raise HTTPException(status_code=404, detail="Education not found")
    return instance


@router.put(
    "/educations/{education_id}",
    response_model=schemas.EducationRead,
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def update_education(
    education_id: int,
    item: schemas.EducationCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    instance = await educations_service.update_education(education_id, data, session)
    if not instance:
        logger.warning("Education %s not found for update", education_id)
        raise HTTPException(status_code=404, detail="Education not found")
    return instance


@router.delete(
    "/educations/{education_id}",
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def delete_education(education_id: int, session: AsyncSession = Depends(get_db)):
    ok = await educations_service.delete_education(education_id, session)
    if not ok:
        logger.warning("Education %s not found for delete", education_id)
        raise HTTPException(status_code=404, detail="Education not found")
    return {"ok": True}
