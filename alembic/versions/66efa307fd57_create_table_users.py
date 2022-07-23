"""create table users

Revision ID: 66efa307fd57
Revises: 679baaa59440
Create Date: 2022-07-21 14:28:22.787397

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import Numeric, Integer


# revision identifiers, used by Alembic.
revision = '66efa307fd57'
down_revision = '679baaa59440'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('last_month_balance', sa.Numeric(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('users')
