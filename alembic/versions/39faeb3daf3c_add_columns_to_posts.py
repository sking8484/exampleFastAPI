"""add columns to posts

Revision ID: 39faeb3daf3c
Revises: 49a9b6b9f589
Create Date: 2022-08-27 17:35:08.604738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39faeb3daf3c'
down_revision = '49a9b6b9f589'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable = False, server_default = '0'))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone = True), nullable = False, server_default = sa.text('now()')
    ))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
