"""empty message

Revision ID: 62d2fa6092df
Revises: 853d38bf3a94
Create Date: 2021-04-12 23:59:18.007258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62d2fa6092df'
down_revision = '853d38bf3a94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user2book',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'book_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user2book')
    # ### end Alembic commands ###
