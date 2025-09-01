from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from ..logger import logger


async def list_portfolio_items(
    profile_id: Optional[int], session: AsyncSession
) -> List[models.PortfolioItem]:
    logger.info("Service: list_portfolio_items profile_id=%s", profile_id)
    filters = [models.PortfolioItem.profile_id == profile_id] if profile_id else None
    return await models.PortfolioItem.list(filters=filters, session=session)


async def create_portfolio_item(data: dict, session: AsyncSession):
    logger.info("Service: create_portfolio_item data=%s", data)
    instance = await models.PortfolioItem.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


async def get_portfolio_item(item_id: int, session: AsyncSession):
    logger.info("Service: get_portfolio_item id=%s", item_id)
    return await models.PortfolioItem.get_by_id(item_id, session=session)


async def update_portfolio_item(item_id: int, data: dict, session: AsyncSession):
    logger.info("Service: update_portfolio_item id=%s data=%s", item_id, data)
    instance = await models.PortfolioItem.update_by_id(item_id, data, session=session)
    if instance:
        await session.commit()
        await session.refresh(instance)
    return instance


async def delete_portfolio_item(item_id: int, session: AsyncSession) -> bool:
    logger.info("Service: delete_portfolio_item id=%s", item_id)
    ok = await models.PortfolioItem.delete_by_id(item_id, session=session)
    if ok:
        await session.commit()
    return ok
