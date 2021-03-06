"""empty message

Revision ID: ac4a431bd896
Revises: fc19e9a99190
Create Date: 2021-11-13 16:18:03.026844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac4a431bd896'
down_revision = 'fc19e9a99190'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_email_key', 'user', type_='unique')
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.create_unique_constraint('user_email_key', 'user', ['email'])
    # ### end Alembic commands ###
