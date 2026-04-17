"""add habit_completions

Revision ID: de3c1fff6bb1
Revises: 74e93b56a103
Create Date: 2026-04-17 14:49:50.004223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de3c1fff6bb1'
down_revision: Union[str, Sequence[str], None] = '74e93b56a103'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
