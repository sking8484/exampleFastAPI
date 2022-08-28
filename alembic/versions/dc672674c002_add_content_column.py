"""add content column

Revision ID: dc672674c002
Revises: aabebd9cd6ac
Create Date: 2022-08-27 17:23:17.125558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc672674c002'
down_revision = 'aabebd9cd6ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(255), nullable = False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
