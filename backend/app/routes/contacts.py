from typing import List

from fastapi import APIRouter, HTTPException, Path

from .. import schemas

router = APIRouter()

_contacts = [
    {"id": 1, "email": "you@example.com", "phone": None, "profile_id": None},
]


@router.get("/contacts", response_model=List[schemas.ContactRead])
async def list_contacts():
    return _contacts


@router.post("/contacts", response_model=schemas.ContactRead)
async def create_contact(item: schemas.ContactCreate):
    next_id = max((c["id"] for c in _contacts), default=0) + 1
    data = item.model_dump()
    data["id"] = next_id
    _contacts.append(data)
    return data


@router.get("/contacts/{contact_id}", response_model=schemas.ContactRead)
async def get_contact(contact_id: int = Path(..., gt=0)):
    for c in _contacts:
        if c["id"] == contact_id:
            return c
    raise HTTPException(status_code=404, detail="Contact not found")


@router.put("/contacts/{contact_id}", response_model=schemas.ContactRead)
async def update_contact(contact_id: int, item: schemas.ContactCreate):
    for idx, c in enumerate(_contacts):
        if c["id"] == contact_id:
            updated = c.copy()
            updated.update(item.model_dump(exclude_unset=True))
            updated["id"] = contact_id
            _contacts[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Contact not found")


@router.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: int):
    for idx, c in enumerate(_contacts):
        if c["id"] == contact_id:
            _contacts.pop(idx)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Contact not found")
