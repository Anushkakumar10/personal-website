from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db

router = APIRouter()


@router.get("/social-links", response_model=List[schemas.SocialLinkRead])
async def list_social_links(session: AsyncSession = Depends(get_db)):
    return await models.SocialLink.list(session=session)


@router.post("/social-links", response_model=schemas.SocialLinkRead)
async def create_social_link(
    item: schemas.SocialLinkCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    instance = await models.SocialLink.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.get("/social-links/{link_id}", response_model=schemas.SocialLinkRead)
async def get_social_link(
    link_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await models.SocialLink.get_by_id(link_id, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Social link not found")
    return instance


@router.put("/social-links/{link_id}", response_model=schemas.SocialLinkRead)
async def update_social_link(
    link_id: int,
    item: schemas.SocialLinkCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    instance = await models.SocialLink.update_by_id(link_id, data, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Social link not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/social-links/{link_id}")
async def delete_social_link(link_id: int, session: AsyncSession = Depends(get_db)):
    ok = await models.SocialLink.delete_by_id(link_id, session=session)
    if not ok:
        raise HTTPException(status_code=404, detail="Social link not found")
    await session.commit()
    return {"ok": True}
