"""Add UserRole

Revision ID: 7d3d70e1ec5f
Revises: 20faf473c64b
Create Date: 2022-10-03 20:33:38.275427

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '7d3d70e1ec5f'
down_revision = '20faf473c64b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    user_role = postgresql.ENUM('super_admin', 'admin', 'user', name='user_role')
    user_role.create(op.get_bind())
    op.add_column('users', sa.Column('role', sa.Enum('super_admin', 'admin', 'user', name='user_role'), server_default='user', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    # ### end Alembic commands ###
