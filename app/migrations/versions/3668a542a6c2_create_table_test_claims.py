"""Create Table test_claims

Revision ID: 3668a542a6c2
Revises: 
Create Date: 2026-10-24 16:36:31.887847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3668a542a6c2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "test_claims",
        sa.Column("ClaimId", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column("ClaimName", sa.VARCHAR(length=200), nullable=False),
        sa.Column("ClaimAmount", sa.FLOAT(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("test_claims")
