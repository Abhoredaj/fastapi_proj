"""add last few columns to posts table

Revision ID: 4486ad242a41
Revises: a3ed3ca31e76
Create Date: 2022-09-15 22:35:27.273808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4486ad242a41'
down_revision = 'a3ed3ca31e76'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
