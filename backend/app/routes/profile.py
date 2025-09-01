from fastapi import APIRouter

from .. import schemas

router = APIRouter()

_profile = {
    "id": 1,
    "name": "Your Name",
    "title": "Software Engineer",
    "location": "Remote",
    "summary": "An example profile generated during scaffolding.",
    "skills": ["python", "fastapi", "sqlalchemy"],
    "projects": [],
    "experiences": [],
    "educations": [],
    "certifications": [],
    "awards": [],
    "publications": [],
    "contacts": [],
    "social_links": [],
    "portfolio_items": [],
    "references": [],
    "skill_items": [],
}


@router.get("/profile", response_model=schemas.ProfileRead)
async def get_profile():
    return _profile


@router.put("/profile", response_model=schemas.ProfileRead)
async def update_profile(profile: schemas.ProfileCreate):
    data = profile.model_dump(exclude_unset=True)
    _profile.update(data)
    return _profile
