from typing import List

from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, models
from ..db import get_db

router = APIRouter()


@router.get("/awards", response_model=List[schemas.AwardRead])
async def list_awards(session: AsyncSession = Depends(get_db)):
    return await models.Award.list(session=session)


@router.post("/awards", response_model=schemas.AwardRead)
async def create_award(
    item: schemas.AwardCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    instance = await models.Award.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.get("/awards/{award_id}", response_model=schemas.AwardRead)
async def get_award(
    award_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await models.Award.get_by_id(award_id, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Award not found")
    return instance


@router.put("/awards/{award_id}", response_model=schemas.AwardRead)
async def update_award(
    award_id: int, item: schemas.AwardCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump(exclude_unset=True)
    instance = await models.Award.update_by_id(award_id, data, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Award not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/awards/{award_id}")
async def delete_award(award_id: int, session: AsyncSession = Depends(get_db)):
    ok = await models.Award.delete_by_id(award_id, session=session)
    if not ok:
        raise HTTPException(status_code=404, detail="Award not found")
    await session.commit()
    return {"ok": True}
