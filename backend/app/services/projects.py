from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from ..logger import logger


async def list_projects(
    profile_id: Optional[int], skill: Optional[str], session: AsyncSession
) -> List[models.Project]:
    logger.info("Service: list_projects (skill=%s profile_id=%s)", skill, profile_id)
    filters = []
    if profile_id:
        filters.append(models.Project.profile_id == profile_id)
    if skill:
        # keep the original .any(skill) behavior
        filters.append(models.Project.skills.any(skill))
    return await models.Project.list(filters=filters or None, session=session)


async def create_project(data: dict, session: AsyncSession) -> models.Project:
    logger.info("Service: create_project data=%s", data)
    instance = await models.Project.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


async def get_project(project_id: int, session: AsyncSession):
    logger.info("Service: get_project id=%s", project_id)
    return await models.Project.get_by_id(project_id, session=session)


async def update_project(project_id: int, data: dict, session: AsyncSession):
    logger.info("Service: update_project id=%s data=%s", project_id, data)
    instance = await models.Project.update_by_id(project_id, data, session=session)
    if instance:
        await session.commit()
        await session.refresh(instance)
    return instance


async def delete_project(project_id: int, session: AsyncSession) -> bool:
    logger.info("Service: delete_project id=%s", project_id)
    ok = await models.Project.delete_by_id(project_id, session=session)
    if ok:
        await session.commit()
    return ok
