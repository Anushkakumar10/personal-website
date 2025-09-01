from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from app.logger import logger


async def list_references(
    profile_id: Optional[int],
    page: int = 1,
    per_page: int = 20,
    session: AsyncSession = None,
) -> List[models.Reference]:
    logger.info(
        "Service: list_references (profile_id=%s page=%s per_page=%s)",
        profile_id,
        page,
        per_page,
    )
    filters = [models.Reference.profile_id == profile_id] if profile_id else None
    limit = min(per_page, 100)
    offset = (page - 1) * limit
    return await models.Reference.list(
        filters=filters, limit=limit, offset=offset, session=session
    )


async def create_reference(data: dict, session: AsyncSession) -> models.Reference:
    logger.info("Service: create_reference data=%s", data)
    instance = await models.Reference.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


async def get_reference(ref_id: int, session: AsyncSession):
    logger.info("Service: get_reference id=%s", ref_id)
    return await models.Reference.get_by_id(ref_id, session=session)


async def update_reference(ref_id: int, data: dict, session: AsyncSession):
    logger.info("Service: update_reference id=%s data=%s", ref_id, data)
    instance = await models.Reference.update_by_id(ref_id, data, session=session)
    if instance:
        await session.commit()
        await session.refresh(instance)
    return instance


async def delete_reference(ref_id: int, session: AsyncSession) -> bool:
    logger.info("Service: delete_reference id=%s", ref_id)
    ok = await models.Reference.delete_by_id(ref_id, session=session)
    if ok:
        await session.commit()
    return ok
