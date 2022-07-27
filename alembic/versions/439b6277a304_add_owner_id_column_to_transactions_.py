"""add owner_id column to transactions, categories, and headers tables

Revision ID: 439b6277a304
Revises: 66efa307fd57
Create Date: 2022-07-23 14:05:31.864007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '439b6277a304'
down_revision = '66efa307fd57'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('transactions', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('transactions_users_fk', source_table="transactions", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")

    op.add_column('categories', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('categories_users_fk', source_table="categories", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")

    op.add_column('headers', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('headers_users_fk', source_table="headers", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")

def downgrade() -> None:
    op.drop_constraint('transactions_users_fk', table_name='transactions')
    op.drop_column('transactions', 'owner_id')

    op.drop_constraint('categories_users_fk', table_name='categories')
    op.drop_column('categories', 'owner_id')

    op.drop_constraint('headers_users_fk', table_name='headers')
    op.drop_column('headers', 'owner_id')
