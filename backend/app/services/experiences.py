from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from app.logger import logger


async def list_experiences(
    profile_id: Optional[int], session: AsyncSession
) -> List[models.Experience]:
    logger.info("Service: list_experiences profile_id=%s", profile_id)
    filters = [models.Experience.profile_id == profile_id] if profile_id else None
    return await models.Experience.list(filters=filters, session=session)


async def create_experience(data: dict, session: AsyncSession):
    logger.info("Service: create_experience data=%s", data)
    instance = await models.Experience.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


async def get_experience(experience_id: int, session: AsyncSession):
    logger.info("Service: get_experience id=%s", experience_id)
    return await models.Experience.get_by_id(experience_id, session=session)


async def update_experience(experience_id: int, data: dict, session: AsyncSession):
    logger.info("Service: update_experience id=%s data=%s", experience_id, data)
    instance = await models.Experience.update_by_id(
        experience_id, data, session=session
    )
    if instance:
        await session.commit()
        await session.refresh(instance)
    return instance


async def delete_experience(experience_id: int, session: AsyncSession) -> bool:
    logger.info("Service: delete_experience id=%s", experience_id)
    ok = await models.Experience.delete_by_id(experience_id, session=session)
    if ok:
        await session.commit()
    return ok
