"""add planned and goal columns to categories table

Revision ID: ddc0c9b43af9
Revises: 900a850e7b68
Create Date: 2022-07-01 18:45:37.974582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddc0c9b43af9'
down_revision = '900a850e7b68'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('categories',
    sa.Column('planned', sa.Numeric(), nullable=False),)

    op.add_column('categories',
    sa.Column('goal', sa.Numeric(), nullable=False),)


def downgrade() -> None:
    op.drop_column('categories', 'planned')
    op.drop_column('categories', 'goal')
