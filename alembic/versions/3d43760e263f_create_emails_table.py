"""create emails table

Revision ID: 3d43760e263f
Revises: 
Create Date: 2024-07-26 16:40:26.275799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d43760e263f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "emails",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            primary_key=True,
            index=True,
            nullable=False,
        ),        sa.Column("sender", sa.String(150), nullable=False),
        sa.Column("recipient", sa.String(150), nullable=False),
        sa.Column("subject", sa.String, nullable=False),
        sa.Column("body", sa.String, nullable=False),
        sa.Column("is_read", sa.Boolean, default=False, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table("emails")
