"""empty message

Revision ID: 94dcead0405e
Revises: 5f0e8389bde9
Create Date: 2021-04-02 03:06:40.908833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94dcead0405e'
down_revision = '5f0e8389bde9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('active__chat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('one_id', sa.Integer(), nullable=True),
    sa.Column('two_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['one_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['two_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('active__chat')
    # ### end Alembic commands ###
