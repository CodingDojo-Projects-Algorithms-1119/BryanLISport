"""empty message

Revision ID: 2600e4d803d4
Revises: 
Create Date: 2019-11-08 15:01:31.260544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2600e4d803d4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_name', sa.String(length=55), nullable=True),
    sa.Column('info', sa.String(length=500), nullable=True),
    sa.Column('participants', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=55), nullable=True),
    sa.Column('last_name', sa.String(length=55), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=150), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_and_events',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'event_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_and_events')
    op.drop_table('message')
    op.drop_table('user')
    op.drop_table('event')
    # ### end Alembic commands ###
