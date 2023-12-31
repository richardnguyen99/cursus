"""add user authentication tables

Revision ID: cf1ffe59d046
Revises: 8190250b81c5
Create Date: 2023-11-15 15:11:32.088341

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "cf1ffe59d046"
down_revision = "8190250b81c5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=11), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=True),
        sa.Column("email", sa.String(length=256), nullable=True),
        sa.Column(
            "emailVerifiedDate", sa.DateTime(timezone=True), nullable=True
        ),
        sa.Column("image", sa.String(length=256), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_users_email"), ["email"], unique=True
        )
        batch_op.create_index(
            batch_op.f("ix_users_name"), ["name"], unique=False
        )

    op.create_table(
        "accounts",
        sa.Column("id", sa.String(length=11), nullable=False),
        sa.Column("type", sa.String(length=256), nullable=False),
        sa.Column("provider", sa.String(length=256), nullable=False),
        sa.Column("providerAccountId", sa.String(length=256), nullable=False),
        sa.Column("refresh_token", sa.Text(), nullable=True),
        sa.Column("access_token", sa.Text(), nullable=True),
        sa.Column("expires_at", sa.Integer(), nullable=True),
        sa.Column("token_type", sa.String(length=64), nullable=True),
        sa.Column("scope", sa.String(length=256), nullable=True),
        sa.Column("id_token", sa.Text(), nullable=True),
        sa.Column("session_state", sa.String(length=256), nullable=True),
        sa.Column("userId", sa.String(length=11), nullable=False),
        sa.ForeignKeyConstraint(["userId"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("accounts", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_accounts_userId"), ["userId"], unique=False
        )

    op.create_table(
        "session",
        sa.Column("id", sa.String(length=11), nullable=False),
        sa.Column("expires", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sessionToken", sa.String(length=256), nullable=False),
        sa.Column("userId", sa.String(length=11), nullable=False),
        sa.ForeignKeyConstraint(["userId"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sessionToken"),
    )
    with op.batch_alter_table("session", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_session_userId"), ["userId"], unique=False
        )

    op.create_table(
        "verification_token",
        sa.Column("id", sa.String(length=11), nullable=False),
        sa.Column("token", sa.String(length=512), nullable=False),
        sa.Column("expires", sa.DateTime(), nullable=False),
        sa.Column("userId", sa.String(length=11), nullable=False),
        sa.ForeignKeyConstraint(["userId"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    with op.batch_alter_table("verification_token", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_verification_token_userId"),
            ["userId"],
            unique=False,
        )

    with op.batch_alter_table("university_campuses", schema=None) as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=postgresql.TIMESTAMP(timezone=True),
            nullable=True,
            existing_server_default=sa.text("now()"),
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("university_campuses", schema=None) as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("verification_token", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_verification_token_userId"))

    op.drop_table("verification_token")
    with op.batch_alter_table("session", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_session_userId"))

    op.drop_table("session")
    with op.batch_alter_table("accounts", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_accounts_userId"))

    op.drop_table("accounts")
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_users_name"))
        batch_op.drop_index(batch_op.f("ix_users_email"))

    op.drop_table("users")
    # ### end Alembic commands ###
