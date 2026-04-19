"""add habit logs

Revision ID: 80d25190dc68
Revises: de3c1fff6bb1
Create Date: 2026-04-19 15:12:09.077619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80d25190dc68'
down_revision: Union[str, Sequence[str], None] = 'de3c1fff6bb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
