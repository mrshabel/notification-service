from src.models.database import database
from src.models.tables.emails import EmailsTable
from src.schemas.email import CreateEmailSchema, EmailSchema
from sqlalchemy.sql.expression import Insert, Select
from sqlalchemy import func, desc
from databases.interfaces import Record
from pydantic import UUID4


@database.transaction()
async def add_one_email(data: CreateEmailSchema) -> EmailSchema:
    """Add one email

    Args:
        data (CreateEmailSchema): The input data

    Returns:
        EmailSchema: The new email record
    """
    query: Insert = EmailsTable.insert().values(**vars(data))
    id: UUID4 = await database.execute(query=query)

    return EmailSchema(id=id, **vars(data))


async def get_one_email_by_id(id: UUID4) -> EmailSchema | None:
    """Get one email by id

    Args:
        id (UUID4): The record id

    Returns:
        EmailSchema | None: The email record if found else nothing
    """

    query: Select = EmailsTable.select().where(EmailsTable.c.id == id)
    record: Record | None = await database.fetch_one(query=query)

    if not record:
        return None
    return EmailSchema(**record._mapping)


async def get_all_emails(
    skip: int, limit: int
) -> tuple[list[EmailSchema], int]:
    """Get one email by id

    Args:
        skip (int): The number of records to skip
        limit (int): The number of records to select

    Returns:
        list[EmailSchema]: A list of emails and the total number of matching records
    """

    query: Select = EmailsTable.select().with_only_columns(
        *[func.count(EmailsTable.c.id)]
    )
    count: int = await database.execute(query=query)

    # fetch records
    query = (
        EmailsTable.select()
        .order_by(desc(EmailsTable.c.created_at))
        .offset(skip)
        .limit(limit)
    )

    # Fetch multiple rows without loading them all into memory at once
    records: list[EmailSchema] = []
    # row: Record

    async for row in database.iterate(query=query):
        records.append(EmailSchema(**row))

    return records, count
