from sqlalchemy import Column, ForeignKey, Integer, String, Table
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
