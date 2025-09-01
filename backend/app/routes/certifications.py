from typing import List

from fastapi import APIRouter, HTTPException, Path

from .. import schemas

router = APIRouter()

_certifications = [
    {"id": 1, "name": "Cert A", "issuer": "Issuer", "profile_id": None},
]


@router.get("/certifications", response_model=List[schemas.CertificationRead])
async def list_certifications():
    return _certifications


@router.post("/certifications", response_model=schemas.CertificationRead)
async def create_certification(item: schemas.CertificationCreate):
    next_id = max((c["id"] for c in _certifications), default=0) + 1
    data = item.model_dump()
    data["id"] = next_id
    _certifications.append(data)
    return data


@router.get("/certifications/{cert_id}", response_model=schemas.CertificationRead)
async def get_certification(cert_id: int = Path(..., gt=0)):
    for c in _certifications:
        if c["id"] == cert_id:
            return c
    raise HTTPException(status_code=404, detail="Certification not found")


@router.put("/certifications/{cert_id}", response_model=schemas.CertificationRead)
async def update_certification(cert_id: int, item: schemas.CertificationCreate):
    for idx, c in enumerate(_certifications):
        if c["id"] == cert_id:
            updated = c.copy()
            updated.update(item.model_dump(exclude_unset=True))
            updated["id"] = cert_id
            _certifications[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Certification not found")


@router.delete("/certifications/{cert_id}")
async def delete_certification(cert_id: int):
    for idx, c in enumerate(_certifications):
        if c["id"] == cert_id:
            _certifications.pop(idx)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Certification not found")
