from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from ..db import get_db
from ..logger import logger
from ..services import social_links as social_links_service

router = APIRouter()


@router.get(
    "/social-links",
    response_model=List[schemas.SocialLinkRead],
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def list_social_links(
    profile_id: int = Query(None, gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Listing social links (profile_id=%s)", profile_id)
    return await social_links_service.list_social_links(profile_id, session)


@router.post(
    "/social-links",
    response_model=schemas.SocialLinkRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def create_social_link(
    item: schemas.SocialLinkCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    logger.info("Creating social link with data=%s", data)
    return await social_links_service.create_social_link(data, session)


@router.get(
    "/social-links/{link_id}",
    response_model=schemas.SocialLinkRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def get_social_link(
    link_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Fetching social link id=%s", link_id)
    instance = await social_links_service.get_social_link(link_id, session)
    if not instance:
        logger.warning("Social link %s not found", link_id)
        raise HTTPException(status_code=404, detail="Social link not found")
    return instance


@router.put(
    "/social-links/{link_id}",
    response_model=schemas.SocialLinkRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def update_social_link(
    link_id: int,
    item: schemas.SocialLinkCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    logger.info("Updating social link id=%s with data=%s", link_id, data)
    instance = await social_links_service.update_social_link(link_id, data, session)
    if not instance:
        logger.warning("Social link %s not found for update", link_id)
        raise HTTPException(status_code=404, detail="Social link not found")
    return instance


@router.delete(
    "/social-links/{link_id}",
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def delete_social_link(link_id: int, session: AsyncSession = Depends(get_db)):
    logger.info("Deleting social link id=%s", link_id)
    ok = await social_links_service.delete_social_link(link_id, session)
    if not ok:
        logger.warning("Social link %s not found for delete", link_id)
        raise HTTPException(status_code=404, detail="Social link not found")
    return {"ok": True}
