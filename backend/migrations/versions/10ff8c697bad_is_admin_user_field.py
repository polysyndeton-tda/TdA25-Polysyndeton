"""is_admin user field

Revision ID: 10ff8c697bad
Revises: cc6b362d2f09
Create Date: 2025-02-18 22:46:44.746427

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "10ff8c697bad"
down_revision = "cc6b362d2f09"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("is_admin", sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("is_admin")

    # ### end Alembic commands ###
