from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db

router = APIRouter()


@router.get("/skills/top", response_model=List[schemas.SkillRead])
async def top_skills(limit: int = 10, session: AsyncSession = Depends(get_db)):
    return await models.Skill.list(limit=limit, session=session)


@router.get("/skills/search", response_model=List[schemas.SkillRead])
async def search_skills(q: str = Query(...), session: AsyncSession = Depends(get_db)):
    return await models.Skill.list(
        filters=[models.Skill.name.ilike(f"%{q}%")], session=session
    )


@router.get("/skills", response_model=List[schemas.SkillRead])
async def list_skills(session: AsyncSession = Depends(get_db)):
    return await models.Skill.list(session=session)


@router.post("/skills", response_model=schemas.SkillRead)
async def create_skill(
    skill: schemas.SkillCreate, session: AsyncSession = Depends(get_db)
):
    data = skill.model_dump()
    instance = await models.Skill.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.get("/skills/{skill_id}", response_model=schemas.SkillRead)
async def get_skill(
    skill_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await models.Skill.get_by_id(skill_id, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Skill not found")
    return instance


@router.put("/skills/{skill_id}", response_model=schemas.SkillRead)
async def update_skill(
    skill_id: int, skill: schemas.SkillCreate, session: AsyncSession = Depends(get_db)
):
    data = skill.model_dump(exclude_unset=True)
    instance = await models.Skill.update_by_id(skill_id, data, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Skill not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/skills/{skill_id}")
async def delete_skill(skill_id: int, session: AsyncSession = Depends(get_db)):
    ok = await models.Skill.delete_by_id(skill_id, session=session)
    if not ok:
        raise HTTPException(status_code=404, detail="Skill not found")
    await session.commit()
    return {"ok": True}
