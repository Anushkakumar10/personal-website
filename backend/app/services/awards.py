from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from ..logger import logger


async def list_awards(
    profile_id: Optional[int], session: AsyncSession
) -> List[models.Award]:
    logger.info("Service: list_awards profile_id=%s", profile_id)
    filters = [models.Award.profile_id == profile_id] if profile_id else None
    return await models.Award.list(filters=filters, session=session)


async def create_award(data: dict, session: AsyncSession):
    logger.info("Service: create_award data=%s", data)
    instance = await models.Award.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


async def get_award(award_id: int, session: AsyncSession):
    logger.info("Service: get_award id=%s", award_id)
    return await models.Award.get_by_id(award_id, session=session)


async def update_award(award_id: int, data: dict, session: AsyncSession):
    logger.info("Service: update_award id=%s data=%s", award_id, data)
    instance = await models.Award.update_by_id(award_id, data, session=session)
    if instance:
        await session.commit()
        await session.refresh(instance)
    return instance


async def delete_award(award_id: int, session: AsyncSession) -> bool:
    logger.info("Service: delete_award id=%s", award_id)
    ok = await models.Award.delete_by_id(award_id, session=session)
    if ok:
        await session.commit()
    return ok
