"""first revision

Revision ID: 137f1f3f9660
Revises: 
Create Date: 2017-09-27 12:55:37.219930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '137f1f3f9660'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=False),
    sa.Column('stored_on_server', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('station',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=30), nullable=False),
    sa.Column('stream_url', sa.VARCHAR(length=200), nullable=False),
    sa.Column('description_html', sa.VARCHAR(length=500), nullable=True),
    sa.Column('cr_tm', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('station_image',
    sa.Column('station_id', sa.Integer(), nullable=True),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['image_id'], ['image.id'], ),
    sa.ForeignKeyConstraint(['station_id'], ['station.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('station_image')
    op.drop_table('station')
    op.drop_table('image')
    # ### end Alembic commands ###