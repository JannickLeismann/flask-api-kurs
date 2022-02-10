"""empty message

Revision ID: 0877bdde2863
Revises: 9bccc86d9105
Create Date: 2022-02-09 13:59:30.572660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0877bdde2863'
down_revision = '9bccc86d9105'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'job', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'job', type_='foreignkey')
    op.drop_column('job', 'user_id')
    # ### end Alembic commands ###
