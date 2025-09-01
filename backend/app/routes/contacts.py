from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db

router = APIRouter()


@router.get("/contacts", response_model=List[schemas.ContactRead])
async def list_contacts(session: AsyncSession = Depends(get_db)):
    return await models.Contact.list(session=session)


@router.post("/contacts", response_model=schemas.ContactRead)
async def create_contact(
    item: schemas.ContactCreate, session: AsyncSession = Depends(get_db)
):
    data = item.model_dump()
    instance = await models.Contact.create(data, session=session)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.get("/contacts/{contact_id}", response_model=schemas.ContactRead)
async def get_contact(
    contact_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    instance = await models.Contact.get_by_id(contact_id, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Contact not found")
    return instance


@router.put("/contacts/{contact_id}", response_model=schemas.ContactRead)
async def update_contact(
    contact_id: int,
    item: schemas.ContactCreate,
    session: AsyncSession = Depends(get_db),
):
    data = item.model_dump(exclude_unset=True)
    instance = await models.Contact.update_by_id(contact_id, data, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Contact not found")
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: int, session: AsyncSession = Depends(get_db)):
    ok = await models.Contact.delete_by_id(contact_id, session=session)
    if not ok:
        raise HTTPException(status_code=404, detail="Contact not found")
    await session.commit()
    return {"ok": True}
