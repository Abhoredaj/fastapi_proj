"""add content column to posts table

Revision ID: 8ba5d31ea5b4
Revises: ac4707696081
Create Date: 2022-09-14 21:07:16.664062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ba5d31ea5b4'
down_revision = 'ac4707696081'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
