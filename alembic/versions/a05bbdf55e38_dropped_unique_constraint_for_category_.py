"""dropped unique constraint for category column in transactions table

Revision ID: a05bbdf55e38
Revises: fe293c75a6d3
Create Date: 2022-07-16 10:24:13.647415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a05bbdf55e38'
down_revision = 'fe293c75a6d3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint('transactions_category_key', 'transactions', type_='unique')


def downgrade() -> None:
    op.create_unique_constraint('transactions_category_key', 'transactions', ['category'])
