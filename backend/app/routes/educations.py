from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db

router = APIRouter()


@router.get("/educations", response_model=List[schemas.EducationRead])
async def list_educations(session: AsyncSession = Depends(get_db)):
    return await models.Education.list(session=session)


@router.post("/educations", response_model=schemas.EducationRead)
async def create_education(
    item: schemas.EducationCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    instance = await models.Education.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.get("/educations/{education_id}", response_model=schemas.EducationRead)
async def get_education(
    education_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await models.Education.get_by_id(education_id, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Education not found")
    return instance


@router.put("/educations/{education_id}", response_model=schemas.EducationRead)
async def update_education(
    education_id: int,
    item: schemas.EducationCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    instance = await models.Education.update_by_id(education_id, data, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Education not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/educations/{education_id}")
async def delete_education(education_id: int, session: AsyncSession = Depends(get_db)):
    ok = await models.Education.delete_by_id(education_id, session=session)
    if not ok:
        raise HTTPException(status_code=404, detail="Education not found")
    await session.commit()
    return {"ok": True}
