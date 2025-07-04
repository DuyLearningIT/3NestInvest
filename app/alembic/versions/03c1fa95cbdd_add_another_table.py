"""add another table

Revision ID: 03c1fa95cbdd
Revises: 2721bcf16059
Create Date: 2025-06-24 14:11:34.076134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03c1fa95cbdd'
down_revision: Union[str, None] = '2721bcf16059'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_change',
    sa.Column('change_id', sa.Integer(), nullable=False),
    sa.Column('change_description', sa.String(length=255), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('requested_by', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('change_id')
    )
    op.create_index(op.f('ix_tb_change_change_id'), 'tb_change', ['change_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tb_change_change_id'), table_name='tb_change')
    op.drop_table('tb_change')
    # ### end Alembic commands ###
