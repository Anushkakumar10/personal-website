from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    skills: List[str] = Field(default_factory=list)


class ProjectCreate(ProjectBase):
    profile_id: Optional[int] = None


class ProjectRead(ProjectBase):
    id: int
    profile_id: Optional[int] = None

    class Config:
        orm_mode = True


class ExperienceBase(BaseModel):
    company: str
    role: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    location: Optional[str] = None
    description: Optional[str] = None
    currently: Optional[bool] = False
    skills: List[str] = Field(default_factory=list)


class ExperienceCreate(ExperienceBase):
    profile_id: int


class ExperienceRead(ExperienceBase):
    id: int
    profile_id: int

    class Config:
        orm_mode = True


class EducationBase(BaseModel):
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    grade: Optional[str] = None
    description: Optional[str] = None


class EducationCreate(EducationBase):
    profile_id: int


class EducationRead(EducationBase):
    id: int
    profile_id: int

    class Config:
        orm_mode = True


class CertificationBase(BaseModel):
    name: str
    issuer: Optional[str] = None
    issue_date: Optional[date] = None
    expiration_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None


class CertificationCreate(CertificationBase):
    profile_id: int


class CertificationRead(CertificationBase):
    id: int
    profile_id: int

    class Config:
        orm_mode = True


class AwardBase(BaseModel):
    title: str
    issuer: Optional[str] = None
    date: Optional[date] = None
    description: Optional[str] = None


class AwardCreate(AwardBase):
    profile_id: int


class AwardRead(AwardBase):
    id: int
    profile_id: int

    class Config:
        orm_mode = True


class PublicationBase(BaseModel):
    title: str
    publisher: Optional[str] = None
    publication_date: Optional[date] = None
    url: Optional[str] = None
    description: Optional[str] = None


class PublicationCreate(PublicationBase):
    profile_id: int


class PublicationRead(PublicationBase):
    id: int
    profile_id: int

    class Config:
        orm_mode = True


class ContactBase(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None


class ContactCreate(ContactBase):
    profile_id: int


class ContactRead(ContactBase):
    id: int
    profile_id: int

    class Config:
        orm_mode = True


class SocialLinkBase(BaseModel):
    platform: Optional[str] = None
    url: Optional[str] = None
    username: Optional[str] = None


class SocialLinkCreate(SocialLinkBase):
    profile_id: int


class SocialLinkRead(SocialLinkBase):
    id: int
    profile_id: int

    class Config:
        orm_mode = True


class PortfolioItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    screenshot_url: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    display_order: Optional[int] = 0


class PortfolioItemCreate(PortfolioItemBase):
    profile_id: int


class PortfolioItemRead(PortfolioItemBase):
    id: int
    profile_id: int

    class Config:
        orm_mode = True


class ReferenceBase(BaseModel):
    name: str
    relation: Optional[str] = None  # matches model attribute name
    contact_info: Optional[str] = None
    testimonial: Optional[str] = None


class ReferenceCreate(ReferenceBase):
    profile_id: int


class ReferenceRead(ReferenceBase):
    id: int
    profile_id: int

    class Config:
        orm_mode = True


class SkillBase(BaseModel):
    name: str
    proficiency: Optional[int] = None
    years: Optional[float] = None


class SkillCreate(SkillBase):
    profile_id: int


class SkillRead(SkillBase):
    id: int
    profile_id: int

    class Config:
        orm_mode = True


class ProfileBase(BaseModel):
    name: str
    title: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = Field(default_factory=list)


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: int
    projects: List[ProjectRead] = Field(default_factory=list)
    experiences: List[ExperienceRead] = Field(default_factory=list)
    educations: List[EducationRead] = Field(default_factory=list)
    certifications: List[CertificationRead] = Field(default_factory=list)
    awards: List[AwardRead] = Field(default_factory=list)
    publications: List[PublicationRead] = Field(default_factory=list)
    contacts: List[ContactRead] = Field(default_factory=list)
    social_links: List[SocialLinkRead] = Field(default_factory=list)
    portfolio_items: List[PortfolioItemRead] = Field(default_factory=list)
    references: List[ReferenceRead] = Field(default_factory=list)
    skill_items: List[SkillRead] = Field(default_factory=list)

    class Config:
        orm_mode = True


class ErrorResponse(BaseModel):
    detail: str
