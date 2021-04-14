"""empty message

Revision ID: 5b87e5fc1253
Revises: 8d31cc30dd4a
Create Date: 2021-03-31 19:09:42.507713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b87e5fc1253'
down_revision = '8d31cc30dd4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('recipient_id', sa.Integer(), nullable=True))
    op.add_column('message', sa.Column('sender_id', sa.Integer(), nullable=True))
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.create_foreign_key(None, 'message', 'user', ['recipient_id'], ['id'])
    op.create_foreign_key(None, 'message', 'user', ['sender_id'], ['id'])
    op.drop_column('message', 'sender')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('sender', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.create_foreign_key(None, 'message', 'user', ['sender'], ['id'])
    op.drop_column('message', 'sender_id')
    op.drop_column('message', 'recipient_id')
    # ### end Alembic commands ###
