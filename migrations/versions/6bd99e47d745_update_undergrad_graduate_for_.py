"""update undergrad & graduate for departments

Revision ID: 6bd99e47d745
Revises: 2911b29178ab
Create Date: 2023-12-20 11:03:08.970656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6bd99e47d745"
down_revision = "2911b29178ab"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("departments", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("undergraduate", sa.Boolean(), nullable=False)
        )
        batch_op.add_column(
            sa.Column("graduate", sa.Boolean(), nullable=False)
        )

    with op.batch_alter_table("universities", schema=None) as batch_op:
        batch_op.drop_index("ix_universities_full_name")
        batch_op.create_index(
            batch_op.f("ix_universities_full_name"), ["full_name"], unique=True
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("universities", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_universities_full_name"))
        batch_op.create_index(
            "ix_universities_full_name",
            [sa.text("lower(full_name::text)")],
            unique=False,
        )

    with op.batch_alter_table("departments", schema=None) as batch_op:
        batch_op.drop_column("graduate")
        batch_op.drop_column("undergraduate")

    # ### end Alembic commands ###
