"""empty message

Revision ID: 2464f298d76d
Revises: b04fefbfe377
Create Date: 2023-07-18 17:03:42.018191

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

import app
# revision identifiers, used by Alembic.
revision = '2464f298d76d'
down_revision = 'b04fefbfe377'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands automate generated by Alembic - please adjust! ###
    with op.batch_alter_table('userdata', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', app.datatypes.SaltyVarChar(length=102), nullable=True))
        batch_op.drop_column('salty_password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands automate generated by Alembic - please adjust! ###
    with op.batch_alter_table('userdata', schema=None) as batch_op:
        batch_op.add_column(sa.Column('salty_password', mysql.VARCHAR(length=102), nullable=True))
        batch_op.drop_column('password')

    # ### end Alembic commands ###
