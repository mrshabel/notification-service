from fastapi import APIRouter, status, HTTPException
from fastapi.logger import logger
from src.schemas import email as email_schemas
from src.models.functions import email as email_functions
from pydantic import UUID4

router = APIRouter(prefix="/emails")


# create email
@router.post("/", response_model=email_schemas.SuccessResponse)
async def add_one_email(req_data: email_schemas.CreateEmailSchema):
    """Add one email"""

    try:
        data: email_schemas.EmailSchema = await email_functions.add_one_email(
            data=req_data
        )
    except BaseException:
        logger.error("Failed to add email", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to add email",
        )

    return email_schemas.SuccessResponse(
        message="Successfully added email", data=data
    )


# get all
@router.get("/", response_model=email_schemas.MultiDataSuccessResponse)
async def get_all_emails(skip: int = 0, limit: int = 10):
    """Get all emails"""
    data: list[email_schemas.EmailSchema]
    count: int

    try:
        data, count = await email_functions.get_all_emails(
            skip=skip, limit=limit
        )
    except BaseException:
        logger.error("Failed to fetch email", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to fetch emails",
        )

    return email_schemas.MultiDataSuccessResponse(
        message="Successfully fetched emails", data=data, count=count
    )


# get by id
@router.get("/{id}/", response_model=email_schemas.SuccessResponse)
async def get_one_email_by_id(skip: int, limit: int, id: UUID4):
    """Get one email by id"""

    try:
        email: email_schemas.EmailSchema | None = (
            await email_functions.get_one_email_by_id(id=id)
        )
    except BaseException:
        logger.error("Failed to fetch email", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to fetch email",
        )

    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email not found"
        )

    return email_schemas.SuccessResponse(
        message="Successfully fetched emails", data=email
    )
