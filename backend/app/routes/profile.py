from fastapi import APIRouter

from .. import schemas

router = APIRouter()

# In-memory placeholder for now
_profile = {
    "name": "Your Name",
    "title": "Software Engineer",
    "location": "Remote",
    "summary": "An example profile generated during scaffolding.",
    "skills": ["python", "fastapi", "sqlalchemy"],
}


@router.get("/profile", response_model=schemas.Profile)
async def get_profile():
    return _profile


@router.put("/profile", response_model=schemas.Profile)
async def update_profile(profile: schemas.Profile):
    _profile.update(profile.dict())
    return _profile
