"""empty message

Revision ID: 2751ac80dc92
Revises: 617a5b745535
Create Date: 2017-11-18 21:42:54.442499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2751ac80dc92'
down_revision = '617a5b745535'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('submit_file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('filepath', sa.String(length=200), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('submit_file')
    # ### end Alembic commands ###