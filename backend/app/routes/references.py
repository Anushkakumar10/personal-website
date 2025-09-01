from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db
from ..logger import logger

router = APIRouter()


@router.get("/references", response_model=List[schemas.ReferenceRead])
async def list_references(
    profile_id: int = Query(None, gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Listing references (profile_id=%s)", profile_id)
    filters = [models.Reference.profile_id == profile_id]
    return await models.Reference.list(filters=filters, session=session)


@router.post("/references", response_model=schemas.ReferenceRead)
async def create_reference(
    item: schemas.ReferenceCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    logger.info("Creating reference with data=%s", data)
    instance = await models.Reference.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    logger.info("Created reference id=%s", getattr(instance, "id", None))
    return instance


@router.get("/references/{ref_id}", response_model=schemas.ReferenceRead)
async def get_reference(
    ref_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Fetching reference id=%s", ref_id)
    instance = await models.Reference.get_by_id(ref_id, session=session)
    if not instance:
        logger.warning("Reference %s not found", ref_id)
        raise HTTPException(status_code=404, detail="Reference not found")
    return instance


@router.put("/references/{ref_id}", response_model=schemas.ReferenceRead)
async def update_reference(
    ref_id: int,
    item: schemas.ReferenceCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    logger.info("Updating reference id=%s data=%s", ref_id, data)
    instance = await models.Reference.update_by_id(ref_id, data, session=session)
    if not instance:
        logger.warning("Reference %s not found for update", ref_id)
        raise HTTPException(status_code=404, detail="Reference not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/references/{ref_id}")
async def delete_reference(ref_id: int, session: AsyncSession = Depends(get_db)):
    logger.info("Deleting reference id=%s", ref_id)
    ok = await models.Reference.delete_by_id(ref_id, session=session)
    if not ok:
        logger.warning("Reference %s not found for delete", ref_id)
        raise HTTPException(status_code=404, detail="Reference not found")
    await session.commit()
    return {"ok": True}
