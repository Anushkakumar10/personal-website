from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from app.db import get_db
from app.services import skills as skills_service

router = APIRouter()


@router.get(
    "/skills/top",
    response_model=List[schemas.SkillRead],
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def top_skills(limit: int = 10, session: AsyncSession = Depends(get_db)):
    return await skills_service.top_skills(limit=limit, session=session)


@router.get(
    "/skills/search",
    response_model=List[schemas.SkillRead],
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def search_skills(q: str = Query(...), session: AsyncSession = Depends(get_db)):
    return await skills_service.search_skills(q=q, session=session)


@router.get(
    "/skills",
    response_model=List[schemas.SkillRead],
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def list_skills(
    profile_id: int = Query(None, gt=0), session: AsyncSession = Depends(get_db)
):
    return await skills_service.list_skills(profile_id, session)


@router.post(
    "/skills",
    response_model=schemas.SkillRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def create_skill(
    skill: schemas.SkillCreate, session: AsyncSession = Depends(get_db)
):
    data = skill.model_dump()
    return await skills_service.create_skill(data, session)


@router.get(
    "/skills/{skill_id}",
    response_model=schemas.SkillRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def get_skill(
    skill_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await skills_service.get_skill(skill_id, session)
    if not instance:
        raise HTTPException(status_code=404, detail="Skill not found")
    return instance


@router.put(
    "/skills/{skill_id}",
    response_model=schemas.SkillRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def update_skill(
    skill_id: int, skill: schemas.SkillCreate, session: AsyncSession = Depends(get_db)
):
    data = skill.model_dump(exclude_unset=True)
    instance = await skills_service.update_skill(skill_id, data, session)
    if not instance:
        raise HTTPException(status_code=404, detail="Skill not found")
    return instance


@router.delete(
    "/skills/{skill_id}",
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def delete_skill(skill_id: int, session: AsyncSession = Depends(get_db)):
    ok = await skills_service.delete_skill(skill_id, session)
    if not ok:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"ok": True}
