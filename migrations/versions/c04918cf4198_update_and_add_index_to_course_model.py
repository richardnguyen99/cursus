"""update and add index to course model

Revision ID: c04918cf4198
Revises: cc6d83c274d5
Create Date: 2023-12-21 15:58:14.312120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c04918cf4198"
down_revision = "cc6d83c274d5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("courses", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("description", sa.String(length=1024), nullable=True)
        )

    op.create_index(
        op.f("ix_courses_title"),
        "courses",
        [sa.text("""LOWER(title) text_pattern_ops""")],
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("courses", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_universities_full_name"))
        batch_op.drop_column("description")

    # ### end Alembic commands ###
