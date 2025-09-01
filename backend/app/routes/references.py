from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db

router = APIRouter()


@router.get("/references", response_model=List[schemas.ReferenceRead])
async def list_references(session: AsyncSession = Depends(get_db)):
    return await models.Reference.list(session=session)


@router.post("/references", response_model=schemas.ReferenceRead)
async def create_reference(
    item: schemas.ReferenceCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    instance = await models.Reference.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.get("/references/{ref_id}", response_model=schemas.ReferenceRead)
async def get_reference(
    ref_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await models.Reference.get_by_id(ref_id, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Reference not found")
    return instance


@router.put("/references/{ref_id}", response_model=schemas.ReferenceRead)
async def update_reference(
    ref_id: int,
    item: schemas.ReferenceCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    instance = await models.Reference.update_by_id(ref_id, data, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Reference not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/references/{ref_id}")
async def delete_reference(ref_id: int, session: AsyncSession = Depends(get_db)):
    ok = await models.Reference.delete_by_id(ref_id, session=session)
    if not ok:
        raise HTTPException(status_code=404, detail="Reference not found")
    await session.commit()
    return {"ok": True}
