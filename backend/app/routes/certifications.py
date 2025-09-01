from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from app.db import get_db
from app.logger import logger
from app.services import certifications as certifications_service

router = APIRouter()


@router.get(
    "/certifications",
    response_model=List[schemas.CertificationRead],
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def list_certifications(
    profile_id: int = Query(None, gt=0), session: AsyncSession = Depends(get_db)
):
    return await certifications_service.list_certifications(profile_id, session)


@router.post(
    "/certifications",
    response_model=schemas.CertificationRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def create_certification(
    item: schemas.CertificationCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    return await certifications_service.create_certification(data, session)


@router.get(
    "/certifications/{cert_id}",
    response_model=schemas.CertificationRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def get_certification(
    cert_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await certifications_service.get_certification(cert_id, session)
    if not instance:
        logger.warning("Certification %s not found", cert_id)
        raise HTTPException(status_code=404, detail="Certification not found")
    return instance


@router.put(
    "/certifications/{cert_id}",
    response_model=schemas.CertificationRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def update_certification(
    cert_id: int,
    item: schemas.CertificationCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    instance = await certifications_service.update_certification(cert_id, data, session)
    if not instance:
        logger.warning("Certification %s not found for update", cert_id)
        raise HTTPException(status_code=404, detail="Certification not found")
    return instance


@router.delete(
    "/certifications/{cert_id}",
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def delete_certification(cert_id: int, session: AsyncSession = Depends(get_db)):
    ok = await certifications_service.delete_certification(cert_id, session)
    if not ok:
        logger.warning("Certification %s not found for delete", cert_id)
        raise HTTPException(status_code=404, detail="Certification not found")
    return {"ok": True}
