"""Added tables supporting profile

Revision ID: 5910e7854713
Revises: ae43e15cf347
Create Date: 2025-09-01 09:18:13.300105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '5910e7854713'
down_revision: Union[str, Sequence[str], None] = 'ae43e15cf347'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create experiences table
    op.create_table(
        "experiences",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("company", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("location", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("currently", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("skills", postgresql.ARRAY(sa.String()), nullable=True),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create educations table
    op.create_table(
        "educations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("institution", sa.String(), nullable=False),
        sa.Column("degree", sa.String(), nullable=True),
        sa.Column("field_of_study", sa.String(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("grade", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create certifications table
    op.create_table(
        "certifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("issuer", sa.String(), nullable=True),
        sa.Column("issue_date", sa.Date(), nullable=True),
        sa.Column("expiration_date", sa.Date(), nullable=True),
        sa.Column("credential_id", sa.String(), nullable=True),
        sa.Column("credential_url", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create awards table
    op.create_table(
        "awards",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("issuer", sa.String(), nullable=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create publications table
    op.create_table(
        "publications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("publisher", sa.String(), nullable=True),
        sa.Column("publication_date", sa.Date(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create contacts table
    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("website", sa.String(), nullable=True),
        sa.Column("address", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create social_links table
    op.create_table(
        "social_links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("platform", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create portfolio_items table
    op.create_table(
        "portfolio_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("screenshot_url", sa.String(), nullable=True),
        sa.Column("skills", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("display_order", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create references table
    op.create_table(
        "references",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("relationship", sa.String(), nullable=True),
        sa.Column("contact_info", sa.String(), nullable=True),
        sa.Column("testimonial", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create skills table
    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("proficiency", sa.Integer(), nullable=True),
        sa.Column("years", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop in reverse order to avoid FK dependency conflicts
    op.drop_table("skills")
    op.drop_table("references")
    op.drop_table("portfolio_items")
    op.drop_table("social_links")
    op.drop_table("contacts")
    op.drop_table("publications")
    op.drop_table("awards")
    op.drop_table("certifications")
    op.drop_table("educations")
    op.drop_table("experiences")
