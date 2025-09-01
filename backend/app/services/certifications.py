from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from app.logger import logger


async def list_certifications(
    profile_id: Optional[int],
    page: int = 1,
    per_page: int = 20,
    session: AsyncSession = None,
) -> List[models.Certification]:
    logger.info(
        "Service: list_certifications profile_id=%s page=%s per_page=%s",
        profile_id,
        page,
        per_page,
    )
    filters = [models.Certification.profile_id == profile_id] if profile_id else None
    limit = min(per_page, 100)
    offset = (page - 1) * limit
    return await models.Certification.list(
        filters=filters, limit=limit, offset=offset, session=session
    )


async def create_certification(data: dict, session: AsyncSession):
    logger.info("Service: create_certification data=%s", data)
    instance = await models.Certification.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


async def get_certification(cert_id: int, session: AsyncSession):
    logger.info("Service: get_certification id=%s", cert_id)
    return await models.Certification.get_by_id(cert_id, session=session)


async def update_certification(cert_id: int, data: dict, session: AsyncSession):
    logger.info("Service: update_certification id=%s data=%s", cert_id, data)
    instance = await models.Certification.update_by_id(cert_id, data, session=session)
    if instance:
        await session.commit()
        await session.refresh(instance)
    return instance


async def delete_certification(cert_id: int, session: AsyncSession) -> bool:
    logger.info("Service: delete_certification id=%s", cert_id)
    ok = await models.Certification.delete_by_id(cert_id, session=session)
    if ok:
        await session.commit()
    return ok
