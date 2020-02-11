"""empty message

Revision ID: caf9114a282b
Revises: 33a26326b791
Create Date: 2020-02-11 14:22:43.699562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'caf9114a282b'
down_revision = '33a26326b791'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shiftArrangement', sa.Column('semester_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'shiftArrangement', 'semester', ['semester_id'], ['id'])
    op.drop_column('shiftArrangement', 'sid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shiftArrangement', sa.Column('sid', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'shiftArrangement', type_='foreignkey')
    op.drop_column('shiftArrangement', 'semester_id')
    # ### end Alembic commands ###
