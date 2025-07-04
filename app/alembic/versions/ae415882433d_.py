""",.

Revision ID: ae415882433d
Revises: 3f690bd979ef
Create Date: 2025-06-27 11:18:10.447041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae415882433d'
down_revision: Union[str, None] = '3f690bd979ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('tb_category_ibfk_1', 'tb_category', type_='foreignkey')
    op.create_foreign_key(None, 'tb_category', 'tb_type', ['type_id'], ['type_id'], ondelete='CASCADE')
    op.drop_constraint('tb_deal_ibfk_1', 'tb_deal', type_='foreignkey')
    op.create_foreign_key(None, 'tb_deal', 'tb_user', ['user_id'], ['user_id'], ondelete='CASCADE')
    op.drop_constraint('tb_order_ibfk_1', 'tb_order', type_='foreignkey')
    op.create_foreign_key(None, 'tb_order', 'tb_deal', ['deal_id'], ['deal_id'], ondelete='CASCADE')
    op.drop_constraint('tb_permission_ibfk_1', 'tb_permission', type_='foreignkey')
    op.create_foreign_key(None, 'tb_permission', 'tb_permission_type', ['permission_type_id'], ['permission_type_id'], ondelete='CASCADE')
    op.drop_constraint('tb_product_ibfk_2', 'tb_product', type_='foreignkey')
    op.create_foreign_key(None, 'tb_product', 'tb_role', ['product_role'], ['role_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tb_product', type_='foreignkey')
    op.create_foreign_key('tb_product_ibfk_2', 'tb_product', 'tb_role', ['product_role'], ['role_id'])
    op.drop_constraint(None, 'tb_permission', type_='foreignkey')
    op.create_foreign_key('tb_permission_ibfk_1', 'tb_permission', 'tb_permission_type', ['permission_type_id'], ['permission_type_id'])
    op.drop_constraint(None, 'tb_order', type_='foreignkey')
    op.create_foreign_key('tb_order_ibfk_1', 'tb_order', 'tb_deal', ['deal_id'], ['deal_id'])
    op.drop_constraint(None, 'tb_deal', type_='foreignkey')
    op.create_foreign_key('tb_deal_ibfk_1', 'tb_deal', 'tb_user', ['user_id'], ['user_id'])
    op.drop_constraint(None, 'tb_category', type_='foreignkey')
    op.create_foreign_key('tb_category_ibfk_1', 'tb_category', 'tb_type', ['type_id'], ['type_id'])
    # ### end Alembic commands ###
