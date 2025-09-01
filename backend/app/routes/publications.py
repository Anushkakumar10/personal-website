from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from app.db import get_db
from app.logger import logger
from app.services import publications as publications_service

router = APIRouter()


@router.get(
    "/publications",
    response_model=List[schemas.PublicationRead],
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def list_publications(
    profile_id: int = Query(None, gt=0),
    page: int = Query(1, gt=0),
    per_page: int = Query(20, gt=1, le=100),
    session: AsyncSession = Depends(get_db),
):
    return await publications_service.list_publications(
        profile_id, page=page, per_page=per_page, session=session
    )


@router.post(
    "/publications",
    response_model=schemas.PublicationRead,
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def create_publication(
    item: schemas.PublicationCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    return await publications_service.create_publication(data, session)


@router.get(
    "/publications/{pub_id}",
    response_model=schemas.PublicationRead,
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def get_publication(
    pub_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await publications_service.get_publication(pub_id, session)
    if not instance:
        logger.warning("Publication %s not found", pub_id)
        raise HTTPException(status_code=404, detail="Publication not found")
    return instance


@router.put(
    "/publications/{pub_id}",
    response_model=schemas.PublicationRead,
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def update_publication(
    pub_id: int,
    item: schemas.PublicationCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    instance = await publications_service.update_publication(pub_id, data, session)
    if not instance:
        logger.warning("Publication %s not found for update", pub_id)
        raise HTTPException(status_code=404, detail="Publication not found")
    return instance


@router.delete(
    "/publications/{pub_id}",
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def delete_publication(pub_id: int, session: AsyncSession = Depends(get_db)):
    ok = await publications_service.delete_publication(pub_id, session)
    if not ok:
        logger.warning("Publication %s not found for delete", pub_id)
        raise HTTPException(status_code=404, detail="Publication not found")
    return {"ok": True}
