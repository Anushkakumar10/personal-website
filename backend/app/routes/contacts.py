from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from app.db import get_db
from app.logger import logger
from app.services import contacts as contacts_service

router = APIRouter()


@router.get(
    "/contacts",
    response_model=List[schemas.ContactRead],
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def list_contacts(
    profile_id: int = Query(None, gt=0),
    page: int = Query(1, gt=0),
    per_page: int = Query(20, gt=1, le=100),
    session: AsyncSession = Depends(get_db),
):
    return await contacts_service.list_contacts(
        profile_id, page=page, per_page=per_page, session=session
    )


@router.post(
    "/contacts",
    response_model=schemas.ContactRead,
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def create_contact(
    item: schemas.ContactCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    return await contacts_service.create_contact(data, session)


@router.get(
    "/contacts/{contact_id}",
    response_model=schemas.ContactRead,
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def get_contact(
    contact_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await contacts_service.get_contact(contact_id, session)
    if not instance:
        logger.warning("Contact %s not found", contact_id)
        raise HTTPException(status_code=404, detail="Contact not found")
    return instance


@router.put(
    "/contacts/{contact_id}",
    response_model=schemas.ContactRead,
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def update_contact(
    contact_id: int,
    item: schemas.ContactCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    instance = await contacts_service.update_contact(contact_id, data, session)
    if not instance:
        logger.warning("Contact %s not found for update", contact_id)
        raise HTTPException(status_code=404, detail="Contact not found")
    return instance


@router.delete(
    "/contacts/{contact_id}",
    responses={
        404: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    },
)
async def delete_contact(contact_id: int, session: AsyncSession = Depends(get_db)):
    ok = await contacts_service.delete_contact(contact_id, session)
    if not ok:
        logger.warning("Contact %s not found for delete", contact_id)
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"ok": True}
