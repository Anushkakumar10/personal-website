from sqlalchemy import Column, ForeignKey, Integer, String, Date, Text, Boolean, Float
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from .db import Base


class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    title = Column(String)
    location = Column(String)
    summary = Column(String)
    skills = Column(ARRAY(String))


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    skills = Column(ARRAY(String))
    profile_id = Column(Integer, ForeignKey("profile.id"))
    profile = relationship("Profile", backref="projects")


class Experience(Base):
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


class Education(Base):
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


class Certification(Base):
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


class Award(Base):
    __tablename__ = "awards"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    title = Column(String, nullable=False)
    issuer = Column(String)
    date = Column(Date)
    description = Column(Text)
    profile = relationship("Profile", backref="awards")


class Publication(Base):
    __tablename__ = "publications"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    title = Column(String, nullable=False)
    publisher = Column(String)
    publication_date = Column(Date)
    url = Column(String)
    description = Column(Text)
    profile = relationship("Profile", backref="publications")


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    email = Column(String)
    phone = Column(String)
    website = Column(String)
    address = Column(String)
    profile = relationship("Profile", backref="contacts")


class SocialLink(Base):
    __tablename__ = "social_links"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    platform = Column(String)  # e.g., linkedin, github, twitter
    url = Column(String)
    username = Column(String)
    profile = relationship("Profile", backref="social_links")


class PortfolioItem(Base):
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


class Reference(Base):
    __tablename__ = "references"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    name = Column(String, nullable=False)
    relation = Column("relationship", String)
    contact_info = Column(String)
    testimonial = Column(Text)
    profile = relationship("Profile", backref="references")


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    name = Column(String, nullable=False)
    proficiency = Column(Integer)  # optional 1-5 scale
    years = Column(Float)  # optional years of experience
    profile = relationship("Profile", backref="skill_items")
