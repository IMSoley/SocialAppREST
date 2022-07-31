"""add foreign-key to posts table

Revision ID: a118da13a785
Revises: bfb5ab9038dd
Create Date: 2022-07-31 11:22:29.076064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a118da13a785'
down_revision = 'bfb5ab9038dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_owner_id_fkey', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_owner_id_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
