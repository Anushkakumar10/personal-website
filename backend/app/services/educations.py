from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from app.logger import logger


async def list_educations(
    profile_id: Optional[int], session: AsyncSession
) -> List[models.Education]:
    logger.info("Service: list_educations profile_id=%s", profile_id)
    filters = [models.Education.profile_id == profile_id] if profile_id else None
    return await models.Education.list(filters=filters, session=session)


async def create_education(data: dict, session: AsyncSession):
    logger.info("Service: create_education data=%s", data)
    instance = await models.Education.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


async def get_education(education_id: int, session: AsyncSession):
    logger.info("Service: get_education id=%s", education_id)
    return await models.Education.get_by_id(education_id, session=session)


async def update_education(education_id: int, data: dict, session: AsyncSession):
    logger.info("Service: update_education id=%s data=%s", education_id, data)
    instance = await models.Education.update_by_id(education_id, data, session=session)
    if instance:
        await session.commit()
        await session.refresh(instance)
    return instance


async def delete_education(education_id: int, session: AsyncSession) -> bool:
    logger.info("Service: delete_education id=%s", education_id)
    ok = await models.Education.delete_by_id(education_id, session=session)
    if ok:
        await session.commit()
    return ok
