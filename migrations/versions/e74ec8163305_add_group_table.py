"""Add Group table

Revision ID: e74ec8163305
Revises: c0ba1cc4523b
Create Date: 2025-01-25 03:14:22.440716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'e74ec8163305'
down_revision: Union[str, None] = 'c0ba1cc4523b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('departments', sa.Column('group_id', sa.String(length=60), nullable=True))
    op.create_foreign_key(None, 'departments', 'groups', ['group_id'], ['id'])
    op.add_column('events', sa.Column('department_id', sa.String(length=60), nullable=True))
    op.add_column('events', sa.Column('group_id', sa.String(length=60), nullable=True))
    op.create_foreign_key(None, 'events', 'departments', ['department_id'], ['id'])
    op.create_foreign_key(None, 'events', 'groups', ['group_id'], ['id'])
    op.add_column('groups', sa.Column('leader_id', sa.String(length=60), nullable=False))
    op.add_column('groups', sa.Column('department_id', sa.String(length=60), nullable=False))
    op.drop_constraint('groups_ibfk_2', 'groups', type_='foreignkey')
    op.drop_constraint('groups_ibfk_1', 'groups', type_='foreignkey')
    op.create_foreign_key(None, 'groups', 'members', ['leader_id'], ['id'])
    op.create_foreign_key(None, 'groups', 'departments', ['department_id'], ['id'])
    op.drop_column('groups', 'head')
    op.drop_column('groups', 'member_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('member_id', mysql.VARCHAR(length=60), nullable=False))
    op.add_column('groups', sa.Column('head', mysql.VARCHAR(length=60), nullable=False))
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.create_foreign_key('groups_ibfk_1', 'groups', 'members', ['member_id'], ['id'])
    op.create_foreign_key('groups_ibfk_2', 'groups', 'members', ['head'], ['id'])
    op.drop_column('groups', 'department_id')
    op.drop_column('groups', 'leader_id')
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_column('events', 'group_id')
    op.drop_column('events', 'department_id')
    op.drop_constraint(None, 'departments', type_='foreignkey')
    op.drop_column('departments', 'group_id')
    # ### end Alembic commands ###
