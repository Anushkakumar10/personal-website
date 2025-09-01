from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, models
from ..db import get_db

router = APIRouter()


@router.get("/profile", response_model=schemas.ProfileRead)
async def get_profile(session: AsyncSession = Depends(get_db)):
    # assume single profile with id=1 as before
    profile = await models.Profile.get_by_id(1, session=session)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # gather related objects (lazy loading isn't available in async)
    projects = await models.Project.list(filters=[models.Project.profile_id == profile.id], session=session)
    experiences = await models.Experience.list(filters=[models.Experience.profile_id == profile.id], session=session)
    educations = await models.Education.list(filters=[models.Education.profile_id == profile.id], session=session)
    certifications = await models.Certification.list(filters=[models.Certification.profile_id == profile.id], session=session)
    awards = await models.Award.list(filters=[models.Award.profile_id == profile.id], session=session)
    publications = await models.Publication.list(filters=[models.Publication.profile_id == profile.id], session=session)
    contacts = await models.Contact.list(filters=[models.Contact.profile_id == profile.id], session=session)
    social_links = await models.SocialLink.list(filters=[models.SocialLink.profile_id == profile.id], session=session)
    portfolio_items = await models.PortfolioItem.list(filters=[models.PortfolioItem.profile_id == profile.id], session=session)
    references = await models.Reference.list(filters=[models.Reference.profile_id == profile.id], session=session)
    skill_items = await models.Skill.list(filters=[models.Skill.profile_id == profile.id], session=session)

    return {
        "id": profile.id,
        "name": profile.name,
        "title": profile.title,
        "location": profile.location,
        "summary": profile.summary,
        "skills": profile.skills or [],
        "projects": projects,
        "experiences": experiences,
        "educations": educations,
        "certifications": certifications,
        "awards": awards,
        "publications": publications,
        "contacts": contacts,
        "social_links": social_links,
        "portfolio_items": portfolio_items,
        "references": references,
        "skill_items": skill_items,
    }


@router.put("/profile", response_model=schemas.ProfileRead)
async def update_profile(profile: schemas.ProfileCreate, session: AsyncSession = Depends(get_db)):
    data = profile.model_dump(exclude_unset=True)
    instance = await models.Profile.update_by_id(1, data, session=session)
    if not instance:
        raise HTTPException(status_code=404, detail="Profile not found")
    await session.commit()
    await session.refresh(instance)

    # return assembled profile as in GET
    return await get_profile(session=session)
