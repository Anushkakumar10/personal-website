from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db

router = APIRouter()


@router.get("/projects", response_model=List[schemas.ProjectRead])
async def list_projects(
    skill: Optional[str] = Query(None), session: AsyncSession = Depends(get_db)
):
    if skill:
        return await models.Project.list(
            filters=[models.Project.skills.any(skill)], session=session
        )
    return await models.Project.list(session=session)


@router.post("/projects", response_model=schemas.ProjectRead)
async def create_project(
    project: schemas.ProjectCreate, session: AsyncSession = Depends(get_db)
):
    data = project.model_dump()
    instance = await models.Project.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.get("/projects/{project_id}", response_model=schemas.ProjectRead)
async def get_project(
    project_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await models.Project.get_by_id(project_id, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Project not found")
    return instance


@router.put("/projects/{project_id}", response_model=schemas.ProjectRead)
async def update_project(
    project_id: int,
    project: schemas.ProjectCreate,
    session: AsyncSession = Depends(get_db),
):
    data = project.model_dump(exclude_unset=True)
    instance = await models.Project.update_by_id(project_id, data, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Project not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/projects/{project_id}")
async def delete_project(project_id: int, session: AsyncSession = Depends(get_db)):
    ok = await models.Project.delete_by_id(project_id, session=session)
    if not ok:
        raise HTTPException(status_code=404, detail="Project not found")
    await session.commit()
    return {"ok": True}
