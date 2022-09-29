"""add last few columns to posts table

Revision ID: 15e4907d9429
Revises: 9faa0e77ca92
Create Date: 2022-09-25 16:16:32.376175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15e4907d9429'
down_revision = '9faa0e77ca92'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'title')
    pass

