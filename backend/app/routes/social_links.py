from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db
from ..logger import logger

router = APIRouter()


@router.get("/social-links", response_model=List[schemas.SocialLinkRead])
async def list_social_links(
    profile_id: int = Query(None, gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Listing social links (profile_id=%s)", profile_id)
    filters = [models.SocialLink.profile_id == profile_id]
    return await models.SocialLink.list(filters=filters, session=session)


@router.post("/social-links", response_model=schemas.SocialLinkRead)
async def create_social_link(
    item: schemas.SocialLinkCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    logger.info("Creating social link with data=%s", data)
    instance = await models.SocialLink.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    logger.info("Created social link id=%s", getattr(instance, "id", None))
    return instance


@router.get("/social-links/{link_id}", response_model=schemas.SocialLinkRead)
async def get_social_link(
    link_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Fetching social link id=%s", link_id)
    instance = await models.SocialLink.get_by_id(link_id, session=session)
    if not instance:
        logger.warning("Social link %s not found", link_id)
        raise HTTPException(status_code=404, detail="Social link not found")
    return instance


@router.put("/social-links/{link_id}", response_model=schemas.SocialLinkRead)
async def update_social_link(
    link_id: int,
    item: schemas.SocialLinkCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    logger.info("Updating social link id=%s with data=%s", link_id, data)
    instance = await models.SocialLink.update_by_id(link_id, data, session=session)
    if not instance:
        logger.warning("Social link %s not found for update", link_id)
        raise HTTPException(status_code=404, detail="Social link not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/social-links/{link_id}")
async def delete_social_link(link_id: int, session: AsyncSession = Depends(get_db)):
    logger.info("Deleting social link id=%s", link_id)
    ok = await models.SocialLink.delete_by_id(link_id, session=session)
    if not ok:
        logger.warning("Social link %s not found for delete", link_id)
        raise HTTPException(status_code=404, detail="Social link not found")
    await session.commit()
    return {"ok": True}
