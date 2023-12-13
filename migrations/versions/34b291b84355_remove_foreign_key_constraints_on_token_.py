"""remove foreign key constraints on token_used

Revision ID: 34b291b84355
Revises: aa1de661b0ce
Create Date: 2023-12-12 20:31:34.287129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34b291b84355'
down_revision = 'aa1de661b0ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.drop_constraint('history_token_used_fkey', type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.create_foreign_key('history_token_used_fkey', 'active_tokens', ['token_used'], ['token'])

    # ### end Alembic commands ###