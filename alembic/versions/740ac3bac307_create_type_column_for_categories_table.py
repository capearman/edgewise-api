"""create 'type' column for categories table

Revision ID: 740ac3bac307
Revises: 27101c046638
Create Date: 2022-07-07 15:38:36.119147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '740ac3bac307'
down_revision = '27101c046638'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('categories', sa.Column('type', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('categories', 'type')
