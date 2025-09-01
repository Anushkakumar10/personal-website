from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db

router = APIRouter()


@router.get("/experiences", response_model=List[schemas.ExperienceRead])
async def list_experiences(session: AsyncSession = Depends(get_db)):
    return await models.Experience.list(session=session)


@router.post("/experiences", response_model=schemas.ExperienceRead)
async def create_experience(
    item: schemas.ExperienceCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    instance = await models.Experience.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.get("/experiences/{experience_id}", response_model=schemas.ExperienceRead)
async def get_experience(
    experience_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await models.Experience.get_by_id(experience_id, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Experience not found")
    return instance


@router.put("/experiences/{experience_id}", response_model=schemas.ExperienceRead)
async def update_experience(
    experience_id: int,
    item: schemas.ExperienceCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    instance = await models.Experience.update_by_id(
        experience_id, data, session=session
    )
    if not instance:
        raise HTTPException(status_code=404, detail="Experience not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/experiences/{experience_id}")
async def delete_experience(
    experience_id: int, session: AsyncSession = Depends(get_db)
):
    ok = await models.Experience.delete_by_id(experience_id, session=session)
    if not ok:
        raise HTTPException(status_code=404, detail="Experience not found")
    await session.commit()
    return {"ok": True}
