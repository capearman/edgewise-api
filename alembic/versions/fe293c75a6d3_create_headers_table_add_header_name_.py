"""create headers table. Add header_name and header_id to categories table.

Revision ID: fe293c75a6d3
Revises: 740ac3bac307
Create Date: 2022-07-08 17:59:21.458302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe293c75a6d3'
down_revision = '740ac3bac307'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('headers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    )
    op.add_column('categories',
    sa.Column('header', sa.String(), nullable=False))
    op.add_column('categories',
    sa.Column('header_id', sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_table('headers')
    op.drop_column('categories', 'header')
    op.drop_column('categories', 'header_id')

