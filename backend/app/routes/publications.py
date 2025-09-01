from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db
from ..logger import logger

router = APIRouter()


@router.get("/publications", response_model=List[schemas.PublicationRead])
async def list_publications(
    profile_id: int = Query(None, gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Listing publications (profile_id=%s)", profile_id)
    filters = [models.Publication.profile_id == profile_id]
    return await models.Publication.list(filters=filters, session=session)


@router.post("/publications", response_model=schemas.PublicationRead)
async def create_publication(
    item: schemas.PublicationCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    logger.info("Creating publication with data=%s", data)
    instance = await models.Publication.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    logger.info("Created publication id=%s", getattr(instance, "id", None))
    return instance


@router.get("/publications/{pub_id}", response_model=schemas.PublicationRead)
async def get_publication(
    pub_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Fetching publication id=%s", pub_id)
    instance = await models.Publication.get_by_id(pub_id, session=session)
    if not instance:
        logger.warning("Publication %s not found", pub_id)
        raise HTTPException(status_code=404, detail="Publication not found")
    return instance


@router.put("/publications/{pub_id}", response_model=schemas.PublicationRead)
async def update_publication(
    pub_id: int,
    item: schemas.PublicationCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    logger.info("Updating publication id=%s data=%s", pub_id, data)
    instance = await models.Publication.update_by_id(pub_id, data, session=session)
    if not instance:
        logger.warning("Publication %s not found for update", pub_id)
        raise HTTPException(status_code=404, detail="Publication not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/publications/{pub_id}")
async def delete_publication(pub_id: int, session: AsyncSession = Depends(get_db)):
    logger.info("Deleting publication id=%s", pub_id)
    ok = await models.Publication.delete_by_id(pub_id, session=session)
    if not ok:
        logger.warning("Publication %s not found for delete", pub_id)
        raise HTTPException(status_code=404, detail="Publication not found")
    await session.commit()
    return {"ok": True}
