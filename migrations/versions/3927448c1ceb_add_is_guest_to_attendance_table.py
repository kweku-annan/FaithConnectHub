"""Add is_guest to attendance table

Revision ID: 3927448c1ceb
Revises: 480edf89b33b
Create Date: 2025-01-24 22:47:05.925048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '3927448c1ceb'
down_revision: Union[str, None] = '480edf89b33b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('attendance', 'member_id',
               existing_type=mysql.VARCHAR(length=60),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('attendance', 'member_id',
               existing_type=mysql.VARCHAR(length=60),
               nullable=False)
    # ### end Alembic commands ###
