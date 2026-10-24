"""Add Column PlaceOfServiceCode

Revision ID: d329a6e9845a
Revises: 3668a542a6c2
Create Date: 2026-10-24 16:57:29.456146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd329a6e9845a'
down_revision: Union[str, Sequence[str], None] = '3668a542a6c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "test_claims",
        sa.Column("PlaceOfServiceCode", sa.VARCHAR(length=50))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("test_claims", "PlaceOfServiceCode")
