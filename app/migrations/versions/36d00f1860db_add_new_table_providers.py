"""Add New Table Providers

Revision ID: 36d00f1860db
Revises: d329a6e9845a
Create Date: 2026-10-24 17:06:18.268464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36d00f1860db'
down_revision: Union[str, Sequence[str], None] = 'd329a6e9845a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "test_provider",
        sa.Column("ProviderId", sa.INTEGER, primary_key = True),
        sa.Column("ProviderName", sa.VARCHAR(length=30),),
        sa.Column("ProviderPlaceOfService", sa.VARCHAR(length=30))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("test_provider")
