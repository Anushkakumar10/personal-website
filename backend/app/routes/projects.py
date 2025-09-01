from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db
from ..logger import logger

router = APIRouter()


@router.get("/projects", response_model=List[schemas.ProjectRead])
async def list_projects(
    profile_id: int = Query(None, gt=0),
    skill: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_db),
):
    logger.info("Listing projects (filter skill=%s profile_id=%s)", skill, profile_id)
    filters = [models.Project.profile_id == profile_id]
    if skill:
        filters.append(models.Project.skills.any(skill))
    return await models.Project.list(filters=filters, session=session)


@router.post("/projects", response_model=schemas.ProjectRead)
async def create_project(
    project: schemas.ProjectCreate, session: AsyncSession = Depends(get_db)
):
    data = project.model_dump()
    logger.info("Creating project with data=%s", data)
    instance = await models.Project.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    logger.info("Created project id=%s", getattr(instance, "id", None))
    return instance


@router.get("/projects/{project_id}", response_model=schemas.ProjectRead)
async def get_project(
    project_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Fetching project id=%s", project_id)
    instance = await models.Project.get_by_id(project_id, session=session)
    if not instance:
        logger.warning("Project %s not found", project_id)
        raise HTTPException(status_code=404, detail="Project not found")
    return instance


@router.put("/projects/{project_id}", response_model=schemas.ProjectRead)
async def update_project(
    project_id: int,
    project: schemas.ProjectCreate,
    session: AsyncSession = Depends(get_db),
):
    data = project.model_dump(exclude_unset=True)
    logger.info("Updating project id=%s data=%s", project_id, data)
    instance = await models.Project.update_by_id(project_id, data, session=session)
    if not instance:
        logger.warning("Project %s not found for update", project_id)
        raise HTTPException(status_code=404, detail="Project not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/projects/{project_id}")
async def delete_project(project_id: int, session: AsyncSession = Depends(get_db)):
    logger.info("Deleting project id=%s", project_id)
    ok = await models.Project.delete_by_id(project_id, session=session)
    if not ok:
        logger.warning("Project %s not found for delete", project_id)
        raise HTTPException(status_code=404, detail="Project not found")
    await session.commit()
    return {"ok": True}
