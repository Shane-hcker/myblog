"""empty message

Revision ID: 88d9d7000bd9
Revises: 631a9e7859e7
Create Date: 2023-08-11 15:15:04.343164

"""
from alembic import op
import sqlalchemy as sa
import app


# revision identifiers, used by Alembic.
revision = '88d9d7000bd9'
down_revision = '631a9e7859e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userdata',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=64), nullable=True),
    sa.Column('username', sa.VARCHAR(length=52), nullable=True),
    sa.Column('avatar', sa.VARCHAR(length=128), nullable=True),
    sa.Column('password', app.datatypes.SaltyVarChar(length=102), nullable=True),
    sa.Column('recent_login', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('following_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['follower_id'], ['userdata.id'], ),
    sa.ForeignKeyConstraint(['following_id'], ['userdata.id'], )
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('post_time', sa.DateTime(), nullable=False),
    sa.Column('poster_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['poster_id'], ['userdata.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_table('followers')
    op.drop_table('userdata')
    # ### end Alembic commands ###