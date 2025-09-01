from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from app.logger import logger


async def list_awards(
    profile_id: Optional[int],
    page: int = 1,
    per_page: int = 20,
    session: AsyncSession = None,
) -> List[models.Award]:
    logger.info(
        "Service: list_awards profile_id=%s page=%s per_page=%s",
        profile_id,
        page,
        per_page,
    )
    filters = [models.Award.profile_id == profile_id] if profile_id else None
    limit = min(per_page, 100)
    offset = (page - 1) * limit
    return await models.Award.list(
        filters=filters, limit=limit, offset=offset, session=session
    )


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
