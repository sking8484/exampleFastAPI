"""Create User Table

Revision ID: 185e91018910
Revises: dc672674c002
Create Date: 2022-08-27 17:26:38.875604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '185e91018910'
down_revision = 'dc672674c002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable = False),
        sa.Column('email', sa.String(255), nullable = False),
        sa.Column('password', sa.String(255), nullable = False),
        sa.Column('created_at', sa.TIMESTAMP(timezone = True),
        server_default = sa.text('now()'),nullable = False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')
