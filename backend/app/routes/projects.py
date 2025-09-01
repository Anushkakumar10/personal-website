from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from app.db import get_db
from app.logger import logger
from app.services import projects as projects_service

router = APIRouter()


@router.get(
    "/projects",
    response_model=List[schemas.ProjectRead],
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def list_projects(
    profile_id: int = Query(None, gt=0),
    skill: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_db),
):
    return await projects_service.list_projects(profile_id, skill, session)


@router.post(
    "/projects",
    response_model=schemas.ProjectRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def create_project(
    project: schemas.ProjectCreate, session: AsyncSession = Depends(get_db)
):
    data = project.model_dump()
    return await projects_service.create_project(data, session)


@router.get(
    "/projects/{project_id}",
    response_model=schemas.ProjectRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def get_project(
    project_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await projects_service.get_project(project_id, session)
    if not instance:
        logger.warning("Project %s not found", project_id)
        raise HTTPException(status_code=404, detail="Project not found")
    return instance


@router.put(
    "/projects/{project_id}",
    response_model=schemas.ProjectRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def update_project(
    project_id: int,
    project: schemas.ProjectCreate,
    session: AsyncSession = Depends(get_db),
):
    data = project.model_dump(exclude_unset=True)
    instance = await projects_service.update_project(project_id, data, session)
    if not instance:
        logger.warning("Project %s not found for update", project_id)
        raise HTTPException(status_code=404, detail="Project not found")
    return instance


@router.delete(
    "/projects/{project_id}",
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def delete_project(project_id: int, session: AsyncSession = Depends(get_db)):
    ok = await projects_service.delete_project(project_id, session)
    if not ok:
        logger.warning("Project %s not found for delete", project_id)
        raise HTTPException(status_code=404, detail="Project not found")
    return {"ok": True}
