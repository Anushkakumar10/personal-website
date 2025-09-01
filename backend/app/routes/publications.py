from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db

router = APIRouter()


@router.get("/publications", response_model=List[schemas.PublicationRead])
async def list_publications(session: AsyncSession = Depends(get_db)):
    return await models.Publication.list(session=session)


@router.post("/publications", response_model=schemas.PublicationRead)
async def create_publication(
    item: schemas.PublicationCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    instance = await models.Publication.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.get("/publications/{pub_id}", response_model=schemas.PublicationRead)
async def get_publication(
    pub_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await models.Publication.get_by_id(pub_id, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Publication not found")
    return instance


@router.put("/publications/{pub_id}", response_model=schemas.PublicationRead)
async def update_publication(
    pub_id: int,
    item: schemas.PublicationCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    instance = await models.Publication.update_by_id(pub_id, data, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Publication not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/publications/{pub_id}")
async def delete_publication(pub_id: int, session: AsyncSession = Depends(get_db)):
    ok = await models.Publication.delete_by_id(pub_id, session=session)
    if not ok:
        raise HTTPException(status_code=404, detail="Publication not found")
    await session.commit()
    return {"ok": True}
