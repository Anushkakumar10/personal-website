from .awards import router as awards
from .certifications import router as certifications
from .contacts import router as contacts
from .educations import router as educations
from .experiences import router as experiences
from .portfolio_items import router as portfolio_items
from .profile import router as profile
from .projects import router as projects
from .publications import router as publications
from .references import router as references
from .skills import router as skills
from .social_links import router as social_links

# list of all routers
routers = [
    awards,
    certifications,
    contacts,
    educations,
    experiences,
    portfolio_items,
    profile,
    projects,
    publications,
    references,
    skills,
    social_links,
]

__all__ = ["routers"]
