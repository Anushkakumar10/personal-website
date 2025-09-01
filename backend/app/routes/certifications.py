from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db

router = APIRouter()


@router.get("/certifications", response_model=List[schemas.CertificationRead])
async def list_certifications(session: AsyncSession = Depends(get_db)):
    return await models.Certification.list(session=session)


@router.post("/certifications", response_model=schemas.CertificationRead)
async def create_certification(
    item: schemas.CertificationCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    instance = await models.Certification.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.get("/certifications/{cert_id}", response_model=schemas.CertificationRead)
async def get_certification(
    cert_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await models.Certification.get_by_id(cert_id, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Certification not found")
    return instance


@router.put("/certifications/{cert_id}", response_model=schemas.CertificationRead)
async def update_certification(
    cert_id: int,
    item: schemas.CertificationCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    instance = await models.Certification.update_by_id(cert_id, data, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Certification not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/certifications/{cert_id}")
async def delete_certification(cert_id: int, session: AsyncSession = Depends(get_db)):
    ok = await models.Certification.delete_by_id(cert_id, session=session)
    if not ok:
        raise HTTPException(status_code=404, detail="Certification not found")
    await session.commit()
    return {"ok": True}
