"""Init database

Revision ID: 42c194104c03
Revises: 
Create Date: 2019-06-11 14:00:51.092750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42c194104c03'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('years',
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('digimv_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('year')
    )
    op.create_table('entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('business_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['year'], ['years.year'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('business_id', 'year')
    )
    op.create_table('data_points',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entry_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('value_type', sa.String(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['entry_id'], ['entries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entry_id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.Column('standardized', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('downloaded', sa.Boolean(), nullable=True),
    sa.Column('downloaded_on', sa.DateTime(), nullable=True),
    sa.Column('indexed_on', sa.DateTime(), nullable=True),
    sa.Column('published_on', sa.Date(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['entry_id'], ['entries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('documents')
    op.drop_table('data_points')
    op.drop_table('entries')
    op.drop_table('years')
    # ### end Alembic commands ###
