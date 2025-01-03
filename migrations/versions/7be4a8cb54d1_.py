"""empty message

Revision ID: 7be4a8cb54d1
Revises: 700b498aff73
Create Date: 2025-01-03 13:26:44.375132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7be4a8cb54d1'
down_revision = '700b498aff73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.add_column(sa.Column('board_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'board', ['board_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('board_id')

    # ### end Alembic commands ###
