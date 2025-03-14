"""empty message

Revision ID: 329f22f69f5e
Revises: 40148db9c7ae
Create Date: 2022-11-08 06:20:20.229639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '329f22f69f5e'
down_revision = '40148db9c7ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transacs', sa.Column('acc', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'transacs', 'accs', ['acc'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transacs', type_='foreignkey')
    op.drop_column('transacs', 'acc')
    # ### end Alembic commands ###
