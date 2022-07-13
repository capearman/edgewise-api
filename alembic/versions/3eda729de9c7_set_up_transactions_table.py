"""set up transactions table

Revision ID: 3eda729de9c7
Revises: 
Create Date: 2022-06-22 11:34:13.689457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3eda729de9c7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table('transactions', 
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('amount', sa.Numeric(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('check_box', sa.Boolean(), nullable=False),
    sa.UniqueConstraint('category'),)


def downgrade() -> None:
    op.drop_table('transactions')
