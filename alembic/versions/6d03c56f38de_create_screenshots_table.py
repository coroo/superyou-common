"""create screenshots table

Revision ID: 6d03c56f38de
Revises: 016712d9f3f4
Create Date: 2021-03-15 19:18:49.953984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d03c56f38de'
down_revision = '016712d9f3f4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'screenshots',
        sa.Column('id', sa.String(50), primary_key=True, index=True),
        sa.Column('url', sa.String(255), nullable=False),
        sa.Column('directory', sa.String(191), nullable=True),
        sa.Column('file_extension', sa.String(20), nullable=True),

        sa.Column('created_at', sa.DateTime(),
                  server_default=sa.func.current_timestamp(), nullable=False),
        sa.Column('updated_at', sa.DateTime(),
                  server_default=sa.func.current_timestamp(), nullable=False),
    )
    pass


def downgrade():
    op.drop_table('screenshots')
    pass
