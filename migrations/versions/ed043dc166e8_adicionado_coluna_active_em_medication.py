"""adicionado coluna active em Medication

Revision ID: ed043dc166e8
Revises: 58fb88274ce8
Create Date: 2025-06-21 11:24:49.174973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed043dc166e8'
down_revision = '58fb88274ce8'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('medications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade():
    with op.batch_alter_table('medications', schema=None) as batch_op:
        batch_op.drop_column('active')

    # ### end Alembic commands ###
