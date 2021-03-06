"""empty message

Revision ID: 8d31cc30dd4a
Revises: 412e8f51f443
Create Date: 2021-03-30 23:17:00.674433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d31cc30dd4a'
down_revision = '412e8f51f443'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=300), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['sender'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_timestamp'), 'message', ['timestamp'], unique=False)
    op.add_column('user', sa.Column('last_message_read_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_message_read_time')
    op.drop_index(op.f('ix_message_timestamp'), table_name='message')
    op.drop_table('message')
    # ### end Alembic commands ###
