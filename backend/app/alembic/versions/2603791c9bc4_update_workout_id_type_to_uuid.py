"""Update Workout Id type to UUID

Revision ID: 2603791c9bc4
Revises: 2630fbcf91e7
Create Date: 2025-01-03 23:16:44.458806

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '2603791c9bc4'
down_revision = '2630fbcf91e7'
branch_labels = None
depends_on = None


def upgrade():
    # Ensure uuid-ossp extension is available
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Create a new UUID column with a default UUID value
    op.add_column('workout', sa.Column('new_id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()')))
    op.add_column('workout', sa.Column('new_owner_id', postgresql.UUID(as_uuid=True), nullable=True))

    # Populate the new columns with UUIDs
    op.execute('UPDATE workout SET new_id = uuid_generate_v4()')
    op.execute('UPDATE workout SET new_owner_id = (SELECT new_id FROM "user" WHERE "user".id = workout.owner_id)')

    # Set the new_id as not nullable
    op.alter_column('workout', 'new_id', nullable=False)

    # Drop old columns and rename new columns
    op.drop_constraint('workout_owner_id_fkey', 'workout', type_='foreignkey')
    op.drop_column('workout', 'owner_id')
    op.alter_column('workout', 'new_owner_id', new_column_name='owner_id')

    op.drop_column('workout', 'id')
    op.alter_column('workout', 'new_id', new_column_name='id')

    # Create primary key constraint
    op.create_primary_key('workout_pkey', 'workout', ['id'])

    # Recreate foreign key constraint
    op.create_foreign_key('workout_owner_id_fkey', 'workout', 'user', ['owner_id'], ['id'])


def downgrade():
    # Reverse the upgrade process
    op.add_column('workout', sa.Column('old_id', sa.Integer, autoincrement=True))
    op.add_column('workout', sa.Column('old_owner_id', sa.Integer, nullable=True))

    # Populate the old columns with default values
    # Generate sequences for the integer IDs if not exist
    op.execute('CREATE SEQUENCE IF NOT EXISTS workout_id_seq AS INTEGER OWNED BY workout.old_id')

    op.execute('SELECT setval(\'workout_id_seq\', COALESCE((SELECT MAX(old_id) + 1 FROM workout), 1), false)')

    op.execute('UPDATE workout SET old_id = nextval(\'workout_id_seq\'), old_owner_id = (SELECT old_id FROM "user" WHERE "user".id = workout.owner_id)')

    # Drop new columns and rename old columns back
    op.drop_constraint('workout_owner_id_fkey', 'workout', type_='foreignkey')
    op.drop_column('workout', 'owner_id')
    op.alter_column('workout', 'old_owner_id', new_column_name='owner_id')

    op.drop_column('workout', 'id')
    op.alter_column('workout', 'old_id', new_column_name='id')

    # Create primary key constraint
    op.create_primary_key('workout_pkey', 'workout', ['id'])

    # Recreate foreign key constraint
    op.create_foreign_key('workout_owner_id_fkey', 'workout', 'user', ['owner_id'], ['id'])
