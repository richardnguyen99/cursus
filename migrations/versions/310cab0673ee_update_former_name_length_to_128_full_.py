"""update former_name length to 128 (full_name)

Revision ID: 310cab0673ee
Revises: 06afe4b68ae2
Create Date: 2023-11-05 16:57:32.063883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '310cab0673ee'
down_revision = '06afe4b68ae2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('universities', schema=None) as batch_op:
        batch_op.alter_column('former_name',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=128),
               existing_nullable=True)
        batch_op.alter_column('motto',
               existing_type=sa.VARCHAR(length=256),
               type_=sa.String(length=512),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('universities', schema=None) as batch_op:
        batch_op.alter_column('motto',
               existing_type=sa.String(length=512),
               type_=sa.VARCHAR(length=256),
               existing_nullable=True)
        batch_op.alter_column('former_name',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)

    # ### end Alembic commands ###
