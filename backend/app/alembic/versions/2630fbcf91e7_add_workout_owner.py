"""Add Workout owner

Revision ID: 2630fbcf91e7
Revises: 4bce08bbddc5
Create Date: 2025-01-03 22:37:22.689195

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '2630fbcf91e7'
down_revision = '4bce08bbddc5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('workout', sa.Column('owner_id', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'workout', 'user', ['owner_id'], ['id'], ondelete='CASCADE')



def downgrade():
    op.drop_constraint(None, 'workout', type_='foreignkey')
    op.drop_column('workout', 'owner_id')
