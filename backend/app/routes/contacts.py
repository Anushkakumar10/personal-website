from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db
from ..logger import logger

router = APIRouter()


@router.get("/contacts", response_model=List[schemas.ContactRead])
async def list_contacts(
    profile_id: int = Query(None, gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Listing contacts (profile_id=%s)", profile_id)
    filters = [models.Contact.profile_id == profile_id]
    return await models.Contact.list(filters=filters, session=session)


@router.post("/contacts", response_model=schemas.ContactRead)
async def create_contact(
    item: schemas.ContactCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    logger.info("Creating contact with data=%s", data)
    instance = await models.Contact.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    logger.info("Created contact id=%s", getattr(instance, "id", None))
    return instance


@router.get("/contacts/{contact_id}", response_model=schemas.ContactRead)
async def get_contact(
    contact_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Fetching contact id=%s", contact_id)
    instance = await models.Contact.get_by_id(contact_id, session=session)
    if not instance:
        logger.warning("Contact %s not found", contact_id)
        raise HTTPException(status_code=404, detail="Contact not found")
    return instance


@router.put("/contacts/{contact_id}", response_model=schemas.ContactRead)
async def update_contact(
    contact_id: int,
    item: schemas.ContactCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    logger.info("Updating contact id=%s data=%s", contact_id, data)
    instance = await models.Contact.update_by_id(contact_id, data, session=session)
    if not instance:
        logger.warning("Contact %s not found for update", contact_id)
        raise HTTPException(status_code=404, detail="Contact not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: int, session: AsyncSession = Depends(get_db)):
    logger.info("Deleting contact id=%s", contact_id)
    ok = await models.Contact.delete_by_id(contact_id, session=session)
    if not ok:
        logger.warning("Contact %s not found for delete", contact_id)
        raise HTTPException(status_code=404, detail="Contact not found")
    await session.commit()
    return {"ok": True}
