"""add category_id to transactions table and make it a foreign key for categories table

Revision ID: 27101c046638
Revises: ddc0c9b43af9
Create Date: 2022-07-07 12:18:36.652160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27101c046638'
down_revision = 'ddc0c9b43af9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('transactions', sa.Column('category_id', sa.Integer(), nullable=False))
    op.create_foreign_key('transactions_categories_fk', source_table="transactions", referent_table="categories", local_cols=['category_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('transactions_categories_fk', table_name='transactions')
    op.drop_column('transactions', 'category_id')
