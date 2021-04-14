"""empty message

Revision ID: a8b9e0d9e0fe
Revises: 94dcead0405e
Create Date: 2021-04-02 18:24:49.714720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8b9e0d9e0fe'
down_revision = '94dcead0405e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('active__chats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('one_id', sa.Integer(), nullable=True),
    sa.Column('two_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['one_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['two_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('active__chat')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('active__chat',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('one_id', sa.INTEGER(), nullable=True),
    sa.Column('two_id', sa.INTEGER(), nullable=True),
    sa.Column('active', sa.BOOLEAN(), nullable=False),
    sa.CheckConstraint('active IN (0, 1)'),
    sa.CheckConstraint('active IN (0, 1)'),
    sa.ForeignKeyConstraint(['one_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['two_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('active__chats')
    # ### end Alembic commands ###