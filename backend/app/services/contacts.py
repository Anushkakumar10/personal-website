from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from app.logger import logger


async def list_contacts(
    profile_id: Optional[int], session: AsyncSession
) -> List[models.Contact]:
    logger.info("Service: list_contacts profile_id=%s", profile_id)
    filters = [models.Contact.profile_id == profile_id] if profile_id else None
    return await models.Contact.list(filters=filters, session=session)


async def create_contact(data: dict, session: AsyncSession):
    logger.info("Service: create_contact data=%s", data)
    instance = await models.Contact.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


async def get_contact(contact_id: int, session: AsyncSession):
    logger.info("Service: get_contact id=%s", contact_id)
    return await models.Contact.get_by_id(contact_id, session=session)


async def update_contact(contact_id: int, data: dict, session: AsyncSession):
    logger.info("Service: update_contact id=%s data=%s", contact_id, data)
    instance = await models.Contact.update_by_id(contact_id, data, session=session)
    if instance:
        await session.commit()
        await session.refresh(instance)
    return instance


async def delete_contact(contact_id: int, session: AsyncSession) -> bool:
    logger.info("Service: delete_contact id=%s", contact_id)
    ok = await models.Contact.delete_by_id(contact_id, session=session)
    if ok:
        await session.commit()
    return ok
