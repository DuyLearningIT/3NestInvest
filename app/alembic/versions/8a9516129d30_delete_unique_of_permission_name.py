"""delete unique of permission name

Revision ID: 8a9516129d30
Revises: 0720756941da
Create Date: 2025-06-17 16:06:38.179496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a9516129d30'
down_revision: Union[str, None] = '0720756941da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('permission_name', table_name='tb_permission')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('permission_name', 'tb_permission', ['permission_name'], unique=True)
    # ### end Alembic commands ###
