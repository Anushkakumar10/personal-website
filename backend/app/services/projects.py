from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from app.logger import logger


async def list_projects(
    profile_id: Optional[int],
    skill: Optional[str],
    page: int = 1,
    per_page: int = 20,
    session: AsyncSession = None,
) -> List[models.Project]:
    logger.info(
        "Service: list_projects (skill=%s profile_id=%s page=%s per_page=%s)",
        skill,
        profile_id,
        page,
        per_page,
    )
    filters = []
    if profile_id:
        filters.append(models.Project.profile_id == profile_id)
    if skill:
        # keep the original .any(skill) behavior
        filters.append(models.Project.skills.any(skill))
    limit = min(per_page, 100)
    offset = (page - 1) * limit
    return await models.Project.list(
        filters=filters or None, limit=limit, offset=offset, session=session
    )


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
