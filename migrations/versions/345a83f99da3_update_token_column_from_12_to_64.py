"""update token column from 12 to 64

Revision ID: 345a83f99da3
Revises: 22b0dd0cb763
Create Date: 2023-11-28 10:44:35.041267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "345a83f99da3"
down_revision = "22b0dd0cb763"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("active_tokens", schema=None) as batch_op:
        batch_op.alter_column(
            "token",
            existing_type=sa.VARCHAR(length=12),
            type_=sa.String(length=64),
            existing_nullable=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("active_tokens", schema=None) as batch_op:
        batch_op.alter_column(
            "token",
            existing_type=sa.String(length=64),
            type_=sa.VARCHAR(length=12),
            existing_nullable=False,
        )

    # ### end Alembic commands ###
