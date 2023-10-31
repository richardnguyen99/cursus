"""update unique constraints on university domains

Revision ID: 53fd93622375
Revises: 912e9e1ff978
Create Date: 2023-10-31 15:19:34.361351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53fd93622375'
down_revision = '912e9e1ff978'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('university_domains', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['domain_name', 'school_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('university_domains', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
