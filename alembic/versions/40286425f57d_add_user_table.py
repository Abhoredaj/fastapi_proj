"""add user table

Revision ID: 40286425f57d
Revises: 8ba5d31ea5b4
Create Date: 2022-09-15 22:19:33.436659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40286425f57d'
down_revision = '8ba5d31ea5b4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('email', sa.String(), nullable=False),
                sa.Column('password', sa.String(), nullable=False),
                sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False),
                sa.PrimaryKeyConstraint('id'),
                sa.UniqueConstraint('email')
                )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
