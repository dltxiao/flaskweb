"""empty message

Revision ID: a129ef20747e
Revises: 
Create Date: 2020-05-19 00:38:36.716477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a129ef20747e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('email', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_Users_email'), 'Users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Users_email'), table_name='Users')
    op.drop_column('Users', 'email')
    # ### end Alembic commands ###