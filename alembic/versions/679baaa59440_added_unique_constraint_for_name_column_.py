"""added unique constraint for name column in categories table

Revision ID: 679baaa59440
Revises: a05bbdf55e38
Create Date: 2022-07-16 10:52:06.531122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '679baaa59440'
down_revision = 'a05bbdf55e38'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('categories_name_key', 'categories', ['name'])


def downgrade() -> None:
    op.drop_constraint('categories_name_key', 'categories', type_='unique')