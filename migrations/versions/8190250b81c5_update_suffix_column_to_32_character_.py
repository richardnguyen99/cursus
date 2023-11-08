"""update suffix column to 32 character-length in university-founder relation

Revision ID: 8190250b81c5
Revises: 8f550a0de3ba
Create Date: 2023-11-07 15:39:39.155488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8190250b81c5"
down_revision = "8f550a0de3ba"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("university_founders", schema=None) as batch_op:
        batch_op.alter_column(
            "suffix",
            existing_type=sa.VARCHAR(length=8),
            type_=sa.String(length=32),
            existing_nullable=True,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("university_founders", schema=None) as batch_op:
        batch_op.alter_column(
            "suffix",
            existing_type=sa.String(length=32),
            type_=sa.VARCHAR(length=8),
            existing_nullable=True,
        )

    # ### end Alembic commands ###
