import sqlalchemy as sa

metadata = sa.MetaData()

EmailsTable = sa.Table(
    "emails",
    metadata,
    sa.Column(
        "id",
        sa.UUID(as_uuid=True),
        server_default=sa.text("gen_random_uuid()"),
        primary_key=True,
        index=True,
        nullable=False,
    ),
    sa.Column("sender", sa.String(150), nullable=False),
    sa.Column("recipient", sa.String(150), nullable=False),
    sa.Column("subject", sa.String, nullable=False),
    sa.Column("body", sa.String, nullable=False),
    sa.Column("is_read", sa.Boolean, default=False, nullable=False),
    sa.Column(
        "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
    ),
)
