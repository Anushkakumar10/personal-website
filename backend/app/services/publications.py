from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from ..logger import logger


async def list_publications(
    profile_id: Optional[int], session: AsyncSession
) -> List[models.Publication]:
    logger.info("Service: list_publications (profile_id=%s)", profile_id)
    filters = [models.Publication.profile_id == profile_id] if profile_id else None
    return await models.Publication.list(filters=filters, session=session)


async def create_publication(data: dict, session: AsyncSession) -> models.Publication:
    logger.info("Service: create_publication data=%s", data)
    instance = await models.Publication.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


async def get_publication(pub_id: int, session: AsyncSession):
    logger.info("Service: get_publication id=%s", pub_id)
    return await models.Publication.get_by_id(pub_id, session=session)


async def update_publication(pub_id: int, data: dict, session: AsyncSession):
    logger.info("Service: update_publication id=%s data=%s", pub_id, data)
    instance = await models.Publication.update_by_id(pub_id, data, session=session)
    if instance:
        await session.commit()
        await session.refresh(instance)
    return instance


async def delete_publication(pub_id: int, session: AsyncSession) -> bool:
    logger.info("Service: delete_publication id=%s", pub_id)
    ok = await models.Publication.delete_by_id(pub_id, session=session)
    if ok:
        await session.commit()
    return ok
