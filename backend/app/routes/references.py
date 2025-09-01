from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from ..db import get_db
from ..logger import logger
from ..services import references as references_service

router = APIRouter()


@router.get(
    "/references",
    response_model=List[schemas.ReferenceRead],
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def list_references(
    profile_id: int = Query(None, gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Listing references (profile_id=%s)", profile_id)
    return await references_service.list_references(profile_id, session)


@router.post(
    "/references",
    response_model=schemas.ReferenceRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def create_reference(
    item: schemas.ReferenceCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    logger.info("Creating reference with data=%s", data)
    return await references_service.create_reference(data, session)


@router.get(
    "/references/{ref_id}",
    response_model=schemas.ReferenceRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def get_reference(
    ref_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Fetching reference id=%s", ref_id)
    instance = await references_service.get_reference(ref_id, session)
    if not instance:
        logger.warning("Reference %s not found", ref_id)
        raise HTTPException(status_code=404, detail="Reference not found")
    return instance


@router.put(
    "/references/{ref_id}",
    response_model=schemas.ReferenceRead,
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def update_reference(
    ref_id: int,
    item: schemas.ReferenceCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    logger.info("Updating reference id=%s data=%s", ref_id, data)
    instance = await references_service.update_reference(ref_id, data, session)
    if not instance:
        logger.warning("Reference %s not found for update", ref_id)
        raise HTTPException(status_code=404, detail="Reference not found")
    return instance


@router.delete(
    "/references/{ref_id}",
    responses={404: {"model": schemas.ErrorResponse}, 500: {"model": schemas.ErrorResponse}},
)
async def delete_reference(ref_id: int, session: AsyncSession = Depends(get_db)):
    logger.info("Deleting reference id=%s", ref_id)
    ok = await references_service.delete_reference(ref_id, session)
    if not ok:
        logger.warning("Reference %s not found for delete", ref_id)
        raise HTTPException(status_code=404, detail="Reference not found")
    return {"ok": True}
