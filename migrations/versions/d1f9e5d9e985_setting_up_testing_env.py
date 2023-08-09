"""setting up testing env

Revision ID: d1f9e5d9e985
Revises: b26c695a0df9
Create Date: 2023-08-09 10:20:50.952087

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd1f9e5d9e985'
down_revision = 'b26c695a0df9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('userdata', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
        batch_op.alter_column('username',
               existing_type=mysql.VARCHAR(length=52),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('userdata', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=mysql.VARCHAR(length=52),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)

    # ### end Alembic commands ###
