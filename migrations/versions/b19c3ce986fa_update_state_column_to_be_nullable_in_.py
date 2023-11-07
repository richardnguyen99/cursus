"""update state column to be nullable in university campus relation

Revision ID: b19c3ce986fa
Revises: 3f57e178746b
Create Date: 2023-11-06 21:22:32.575331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b19c3ce986fa'
down_revision = '3f57e178746b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('university_campuses', schema=None) as batch_op:
        batch_op.alter_column('address_state',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('university_campuses', schema=None) as batch_op:
        batch_op.alter_column('address_state',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)

    # ### end Alembic commands ###
