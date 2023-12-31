"""alter short_name to university id on course model

Revision ID: e40f6f874274
Revises: c04918cf4198
Create Date: 2023-12-21 21:15:05.641238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e40f6f874274'
down_revision = 'c04918cf4198'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('credits', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('university_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('courses_code_school_id_key', type_='unique')
        batch_op.drop_index('ix_courses_title')
        batch_op.create_index(batch_op.f('ix_courses_title'), ['title'], unique=False)
        batch_op.create_unique_constraint(None, ['code', 'university_id'])
        batch_op.drop_constraint('courses_school_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'universities', ['university_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
        batch_op.drop_column('school_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('school_id', sa.VARCHAR(length=32), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('courses_school_id_fkey', 'universities', ['school_id'], ['short_name'], onupdate='CASCADE', ondelete='CASCADE')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_index(batch_op.f('ix_courses_title'))
        batch_op.create_index('ix_courses_title', [sa.text('lower(title::text)')], unique=False)
        batch_op.create_unique_constraint('courses_code_school_id_key', ['code', 'school_id'])
        batch_op.drop_column('university_id')
        batch_op.drop_column('credits')

    # ### end Alembic commands ###
