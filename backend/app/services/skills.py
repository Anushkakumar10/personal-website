from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from app.logger import logger


async def top_skills(limit: int, session: AsyncSession) -> List[models.Skill]:
    logger.info("Service: top_skills limit=%s", limit)
    return await models.Skill.list(limit=limit, session=session)


async def search_skills(q: str, session: AsyncSession) -> List[models.Skill]:
    logger.info("Service: search_skills q=%s", q)
    return await models.Skill.list(
        filters=[models.Skill.name.ilike(f"%{q}%")], session=session
    )


async def list_skills(
    profile_id: Optional[int],
    page: int = 1,
    per_page: int = 20,
    session: AsyncSession = None,
) -> List[models.Skill]:
    logger.info(
        "Service: list_skills profile_id=%s page=%s per_page=%s",
        profile_id,
        page,
        per_page,
    )
    filters = [models.Skill.profile_id == profile_id] if profile_id else None
    limit = min(per_page, 100)
    offset = (page - 1) * limit
    return await models.Skill.list(
        filters=filters, limit=limit, offset=offset, session=session
    )


async def create_skill(data: dict, session: AsyncSession) -> models.Skill:
    logger.info("Service: create_skill data=%s", data)
    instance = await models.Skill.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


async def get_skill(skill_id: int, session: AsyncSession):
    logger.info("Service: get_skill id=%s", skill_id)
    return await models.Skill.get_by_id(skill_id, session=session)


async def update_skill(skill_id: int, data: dict, session: AsyncSession):
    logger.info("Service: update_skill id=%s data=%s", skill_id, data)
    instance = await models.Skill.update_by_id(skill_id, data, session=session)
    if instance:
        await session.commit()
        await session.refresh(instance)
    return instance


async def delete_skill(skill_id: int, session: AsyncSession) -> bool:
    logger.info("Service: delete_skill id=%s", skill_id)
    ok = await models.Skill.delete_by_id(skill_id, session=session)
    if ok:
        await session.commit()
    return ok
