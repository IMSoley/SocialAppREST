"""add content column to posts table

Revision ID: 166487ce73bc
Revises: a3409f2f3eec
Create Date: 2022-07-31 11:15:55.756604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '166487ce73bc'
down_revision = 'a3409f2f3eec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
