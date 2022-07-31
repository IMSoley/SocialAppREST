"""create post table

Revision ID: a3409f2f3eec
Revises: 
Create Date: 2022-07-31 11:13:44.153471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3409f2f3eec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
