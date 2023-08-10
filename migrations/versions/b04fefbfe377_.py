"""empty message

Revision ID: b04fefbfe377
Revises: 2de54d025014
Create Date: 2023-07-04 15:16:21.613690

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

import app

# revision identifiers, used by Alembic.
revision = 'b04fefbfe377'
down_revision = '2de54d025014'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands automate generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('post_time', sa.DateTime(), nullable=False),
    sa.Column('poster_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['poster_id'], ['userdata.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('userdata', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recent_login', sa.DateTime(), nullable=True))
        batch_op.alter_column('salty_password',
               existing_type=mysql.VARCHAR(length=64),
               type_=app.datatypes.SaltyVarChar(length=102),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands automate generated by Alembic - please adjust! ###
    with op.batch_alter_table('userdata', schema=None) as batch_op:
        batch_op.alter_column('salty_password',
               existing_type=app.datatypes.SaltyVarChar(length=102),
               type_=mysql.VARCHAR(length=64),
               existing_nullable=True)
        batch_op.drop_column('recent_login')

    op.drop_table('posts')
    # ### end Alembic commands ###
