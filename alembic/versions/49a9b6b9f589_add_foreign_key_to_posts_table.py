"""add foreign key to posts table

Revision ID: 49a9b6b9f589
Revises: 185e91018910
Create Date: 2022-08-27 17:31:20.060664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49a9b6b9f589'
down_revision = '185e91018910'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('posts_users_fk',
    source_table = 'posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name = 'posts')
    op.drop_column('posts', 'owner_id')
