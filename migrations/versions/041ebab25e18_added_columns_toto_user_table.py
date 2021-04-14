"""added columns toto user table

Revision ID: 041ebab25e18
Revises: 77d83587283e
Create Date: 2021-03-06 11:04:50.367587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '041ebab25e18'
down_revision = '77d83587283e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('LS', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('about_me', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'about_me')
    op.drop_column('user', 'LS')
    # ### end Alembic commands ###