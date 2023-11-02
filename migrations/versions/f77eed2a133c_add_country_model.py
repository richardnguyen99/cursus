"""add country model

Revision ID: f77eed2a133c
Revises: 3832df4d229e
Create Date: 2023-11-02 13:17:28.432618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f77eed2a133c'
down_revision = '3832df4d229e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('alpha2', sa.String(length=2), nullable=False),
    sa.Column('alpha3', sa.String(length=3), nullable=False),
    sa.Column('country_code', sa.String(length=3), nullable=False),
    sa.Column('iso3166_2', sa.String(length=16), nullable=False),
    sa.Column('region', sa.String(length=64), nullable=True),
    sa.Column('subregion', sa.String(length=64), nullable=True),
    sa.Column('region_code', sa.String(length=3), nullable=True),
    sa.Column('sub_region_code', sa.String(length=3), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'alpha2', 'alpha3')
    )
    with op.batch_alter_table('countries', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_countries_alpha2'), ['alpha2'], unique=True)
        batch_op.create_index(batch_op.f('ix_countries_alpha3'), ['alpha3'], unique=True)
        batch_op.create_index(batch_op.f('ix_countries_country_code'), ['country_code'], unique=True)
        batch_op.create_index(batch_op.f('ix_countries_iso3166_2'), ['iso3166_2'], unique=True)
        batch_op.create_index(batch_op.f('ix_countries_name'), ['name'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('countries', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_countries_name'))
        batch_op.drop_index(batch_op.f('ix_countries_iso3166_2'))
        batch_op.drop_index(batch_op.f('ix_countries_country_code'))
        batch_op.drop_index(batch_op.f('ix_countries_alpha3'))
        batch_op.drop_index(batch_op.f('ix_countries_alpha2'))

    op.drop_table('countries')
    # ### end Alembic commands ###
