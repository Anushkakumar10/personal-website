from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from app.logger import logger


async def list_social_links(
    profile_id: Optional[int], session: AsyncSession
) -> List[models.SocialLink]:
    # build sensible filters only when profile_id provided
    logger.info("Service: list_social_links (profile_id=%s)", profile_id)
    filters = [models.SocialLink.profile_id == profile_id] if profile_id else None
    return await models.SocialLink.list(filters=filters, session=session)


async def create_social_link(data: dict, session: AsyncSession) -> models.SocialLink:
    logger.info("Service: create_social_link data=%s", data)
    instance = await models.SocialLink.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    logger.info("Service: created social link id=%s", getattr(instance, "id", None))
    return instance


async def get_social_link(
    link_id: int, session: AsyncSession
) -> Optional[models.SocialLink]:
    logger.info("Service: get_social_link id=%s", link_id)
    return await models.SocialLink.get_by_id(link_id, session=session)


async def update_social_link(
    link_id: int, data: dict, session: AsyncSession
) -> Optional[models.SocialLink]:
    logger.info("Service: update_social_link id=%s data=%s", link_id, data)
    instance = await models.SocialLink.update_by_id(link_id, data, session=session)
    if instance:
        await session.commit()
        await session.refresh(instance)
    return instance


async def delete_social_link(link_id: int, session: AsyncSession) -> bool:
    logger.info("Service: delete_social_link id=%s", link_id)
    ok = await models.SocialLink.delete_by_id(link_id, session=session)
    if ok:
        await session.commit()
    return ok
