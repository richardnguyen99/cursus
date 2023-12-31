"""add active column for department model

Revision ID: d82ac9ef7cac
Revises: 6bd99e47d745
Create Date: 2023-12-20 12:46:05.298223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d82ac9ef7cac"
down_revision = "6bd99e47d745"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("departments", schema=None) as batch_op:
        batch_op.add_column(sa.Column("active", sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("departments", schema=None) as batch_op:
        batch_op.drop_column("active")

    # ### end Alembic commands ###
