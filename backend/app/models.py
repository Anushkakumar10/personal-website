from typing import Any, List, Optional, Sequence

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    select,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from .db import AsyncSessionLocal, Base


class CRUDMixin:
    @classmethod
    async def get_by_id(cls, id: Any, session: Optional[AsyncSession] = None):
        if session:
            return await session.get(cls, id)
        async with AsyncSessionLocal() as s:
            return await s.get(cls, id)

    @classmethod
    async def list(
        cls,
        filters: Optional[Sequence] = None,
        offset: int = 0,
        limit: int = 100,
        session: Optional[AsyncSession] = None,
    ) -> List[Any]:
        stmt = select(cls)
        if filters:
            for f in filters:
                stmt = stmt.where(f)
        stmt = stmt.offset(offset).limit(limit)
        if session:
            result = await session.execute(stmt)
            return result.scalars().all()
        async with AsyncSessionLocal() as s:
            result = await s.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def create(cls, values: dict, session: Optional[AsyncSession] = None):
        instance = cls(**values)
        if session:
            session.add(instance)
            # ensure DB-generated fields are available without committing
            await session.flush()
            try:
                await session.refresh(instance)
            except Exception:
                # refresh may fail in some edge cases; ignore and return instance
                pass
            return instance
        async with AsyncSessionLocal() as s:
            s.add(instance)
            await s.commit()
            await s.refresh(instance)
            return instance

    @classmethod
    async def update_by_id(
        cls, id: Any, data: dict, session: Optional[AsyncSession] = None
    ):
        if session:
            instance = await session.get(cls, id)
            if not instance:
                return None
            for k, v in data.items():
                setattr(instance, k, v)
            session.add(instance)
            await session.flush()
            try:
                await session.refresh(instance)
            except Exception:
                pass
            return instance
        async with AsyncSessionLocal() as s:
            instance = await s.get(cls, id)
            if not instance:
                return None
            for k, v in data.items():
                setattr(instance, k, v)
            s.add(instance)
            await s.commit()
            await s.refresh(instance)
            return instance

    @classmethod
    async def delete_by_id(
        cls, id: Any, session: Optional[AsyncSession] = None
    ) -> bool:
        if session:
            instance = await session.get(cls, id)
            if not instance:
                return False
            await session.delete(instance)
            await session.flush()
            return True
        async with AsyncSessionLocal() as s:
            instance = await s.get(cls, id)
            if not instance:
                return False
            await s.delete(instance)
            await s.commit()
            return True

    async def delete(self, session: Optional[AsyncSession] = None) -> None:
        if session:
            await session.delete(self)
            await session.flush()
            return
        async with AsyncSessionLocal() as s:
            await s.delete(self)
            await s.commit()


class Profile(CRUDMixin, Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    title = Column(String)
    location = Column(String)
    summary = Column(String)
    skills = Column(ARRAY(String))


class Project(CRUDMixin, Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    skills = Column(ARRAY(String))
    profile_id = Column(Integer, ForeignKey("profile.id"))
    profile = relationship("Profile", backref="projects")


class Experience(CRUDMixin, Base):
    __tablename__ = "experiences"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    location = Column(String)
    description = Column(Text)
    currently = Column(Boolean, default=False)
    skills = Column(ARRAY(String))
    profile = relationship("Profile", backref="experiences")


class Education(CRUDMixin, Base):
    __tablename__ = "educations"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    institution = Column(String, nullable=False)
    degree = Column(String)
    field_of_study = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    grade = Column(String)
    description = Column(Text)
    profile = relationship("Profile", backref="educations")


class Certification(CRUDMixin, Base):
    __tablename__ = "certifications"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    name = Column(String, nullable=False)
    issuer = Column(String)
    issue_date = Column(Date)
    expiration_date = Column(Date)
    credential_id = Column(String)
    credential_url = Column(String)
    profile = relationship("Profile", backref="certifications")


class Award(CRUDMixin, Base):
    __tablename__ = "awards"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    title = Column(String, nullable=False)
    issuer = Column(String)
    date = Column(Date)
    description = Column(Text)
    profile = relationship("Profile", backref="awards")


class Publication(CRUDMixin, Base):
    __tablename__ = "publications"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    title = Column(String, nullable=False)
    publisher = Column(String)
    publication_date = Column(Date)
    url = Column(String)
    description = Column(Text)
    profile = relationship("Profile", backref="publications")


class Contact(CRUDMixin, Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    email = Column(String)
    phone = Column(String)
    website = Column(String)
    address = Column(String)
    profile = relationship("Profile", backref="contacts")


class SocialLink(CRUDMixin, Base):
    __tablename__ = "social_links"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    platform = Column(String)  # e.g., linkedin, github, twitter
    url = Column(String)
    username = Column(String)
    profile = relationship("Profile", backref="social_links")


class PortfolioItem(CRUDMixin, Base):
    __tablename__ = "portfolio_items"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    url = Column(String)
    screenshot_url = Column(String)
    skills = Column(ARRAY(String))
    display_order = Column(Integer, default=0)
    profile = relationship("Profile", backref="portfolio_items")


class Reference(CRUDMixin, Base):
    __tablename__ = "references"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    name = Column(String, nullable=False)
    relation = Column("relationship", String)
    contact_info = Column(String)
    testimonial = Column(Text)
    profile = relationship("Profile", backref="references")


class Skill(CRUDMixin, Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    name = Column(String, nullable=False)
    proficiency = Column(Integer)  # optional 1-5 scale
    years = Column(Float)  # optional years of experience
    profile = relationship("Profile", backref="skill_items")
