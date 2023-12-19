"""add school model

Revision ID: 52b730737e11
Revises: 80463f6d127e
Create Date: 2023-12-16 14:32:27.515119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "52b730737e11"
down_revision = "80463f6d127e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "schools",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("website", sa.String(length=128), nullable=True),
        sa.Column("university_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "modified_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["university_id"],
            ["universities.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "university_id"),
    )
    with op.batch_alter_table("schools", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_schools_name"), ["name"], unique=False
        )

    with op.batch_alter_table("departments", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("university_id", sa.Integer(), nullable=False)
        )
        batch_op.drop_constraint(
            "departments_school_id_fkey", type_="foreignkey"
        )
        batch_op.create_foreign_key(
            None,
            "schools",
            ["school_id"],
            ["id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
        batch_op.create_foreign_key(
            None,
            "universities",
            ["university_id"],
            ["id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        )

    connection = op.get_bind()
    connection.execute(
        sa.text(
            """
CREATE OR REPLACE FUNCTION insert_school_created_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.created_at = now();
   NEW.modified_at = now();
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE OR REPLACE FUNCTION update_school_modified_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.modified_at = now();
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_school_modifed_at BEFORE UPDATE
ON schools
FOR EACH ROW EXECUTE PROCEDURE update_school_modified_at_column();

CREATE TRIGGER insert_school_created_time BEFORE INSERT
ON schools 
FOR EACH ROW EXECUTE PROCEDURE insert_school_created_at_column();
"""
        )
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("departments", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_foreign_key(
            "departments_school_id_fkey",
            "universities",
            ["school_id"],
            ["id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
        batch_op.drop_column("university_id")

    with op.batch_alter_table("schools", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_schools_name"))

    op.drop_table("schools")
    # ### end Alembic commands ###