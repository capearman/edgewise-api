"""add categories table

Revision ID: 900a850e7b68
Revises: 3eda729de9c7
Create Date: 2022-07-01 18:11:52.532833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '900a850e7b68'
down_revision = '3eda729de9c7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('name', sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('categories')
