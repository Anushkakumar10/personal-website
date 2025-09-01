from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .. import models, schemas
from ..db import get_db
from ..logger import logger

router = APIRouter()


@router.get("/profiles/{profile_id}", response_model=schemas.ProfileRead)
async def get_profile(
    profile_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_db)
):
    logger.info("Fetching profile id=%s", profile_id)

    stmt = (
        select(models.Profile)
        .where(models.Profile.id == profile_id)
        .options(
            selectinload(models.Profile.projects),
            selectinload(models.Profile.experiences),
            selectinload(models.Profile.educations),
            selectinload(models.Profile.certifications),
            selectinload(models.Profile.awards),
            selectinload(models.Profile.publications),
            selectinload(models.Profile.contacts),
            selectinload(models.Profile.social_links),
            selectinload(models.Profile.portfolio_items),
            selectinload(models.Profile.references),
            selectinload(models.Profile.skill_items),
        )
    )
    result = await session.execute(stmt)
    profile = result.scalars().first()

    if not profile:
        logger.warning("Profile id=%s not found", profile_id)
        raise HTTPException(status_code=404, detail="Profile not found")

    logger.debug(
        "Assembled profile id=%s with related counts projects=%d experiences=%d",
        profile.id,
        len(profile.projects),
        len(profile.experiences),
    )
    return {
        "id": profile.id,
        "name": profile.name,
        "title": profile.title,
        "location": profile.location,
        "summary": profile.summary,
        "skills": profile.skills or [],
        "projects": profile.projects,
        "experiences": profile.experiences,
        "educations": profile.educations,
        "certifications": profile.certifications,
        "awards": profile.awards,
        "publications": profile.publications,
        "contacts": profile.contacts,
        "social_links": profile.social_links,
        "portfolio_items": profile.portfolio_items,
        "references": profile.references,
        "skill_items": profile.skill_items,
    }


@router.put("/profiles/{profile_id}", response_model=schemas.ProfileRead)
async def update_profile(
    profile: schemas.ProfileCreate,
    profile_id: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_db),
):
    data = profile.model_dump(exclude_unset=True)
    logger.info("Updating profile id=%s with data=%s", profile_id, data)
    instance = await models.Profile.update_by_id(profile_id, data, session=session)
    if not instance:
        logger.warning("Profile id=%s not found for update", profile_id)
        raise HTTPException(status_code=404, detail="Profile not found")
    await session.commit()
    await session.refresh(instance)

    # return assembled profile as in GET
    return await get_profile(profile_id=profile_id, session=session)
