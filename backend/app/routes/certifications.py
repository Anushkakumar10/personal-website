from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db
from ..logger import logger

router = APIRouter()


@router.get("/certifications", response_model=List[schemas.CertificationRead])
async def list_certifications(
    profile_id: int = Query(None, gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Listing certifications (profile_id=%s)", profile_id)
    filters = [models.Certification.profile_id == profile_id]
    return await models.Certification.list(filters=filters, session=session)


@router.post("/certifications", response_model=schemas.CertificationRead)
async def create_certification(
    item: schemas.CertificationCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    logger.info("Creating certification with data=%s", data)
    instance = await models.Certification.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    logger.info("Created certification id=%s", getattr(instance, "id", None))
    return instance


@router.get("/certifications/{cert_id}", response_model=schemas.CertificationRead)
async def get_certification(
    cert_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Fetching certification id=%s", cert_id)
    instance = await models.Certification.get_by_id(cert_id, session=session)
    if not instance:
        logger.warning("Certification %s not found", cert_id)
        raise HTTPException(status_code=404, detail="Certification not found")
    return instance


@router.put("/certifications/{cert_id}", response_model=schemas.CertificationRead)
async def update_certification(
    cert_id: int,
    item: schemas.CertificationCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    logger.info("Updating certification id=%s data=%s", cert_id, data)
    instance = await models.Certification.update_by_id(cert_id, data, session=session)
    if not instance:
        logger.warning("Certification %s not found for update", cert_id)
        raise HTTPException(status_code=404, detail="Certification not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/certifications/{cert_id}")
async def delete_certification(cert_id: int, session: AsyncSession = Depends(get_db)):
    logger.info("Deleting certification id=%s", cert_id)
    ok = await models.Certification.delete_by_id(cert_id, session=session)
    if not ok:
        logger.warning("Certification %s not found for delete", cert_id)
        raise HTTPException(status_code=404, detail="Certification not found")
    await session.commit()
    return {"ok": True}
