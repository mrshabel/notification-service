from fastapi import APIRouter, status, HTTPException, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.logger import logger
from src.schemas import email as email_schemas
from src.models.functions import email as email_functions
from src.utils import email as email_utils
from pydantic import UUID4

router = APIRouter(prefix="/emails")

templates = Jinja2Templates(directory="templates")


# create email
@router.post("/", response_model=email_schemas.SuccessResponse)
async def add_one_email(
    req_data: email_schemas.CreateEmailSchema,
    background_tasks: BackgroundTasks,
):
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

    try:
        # send email to recipient
        name = "Test Client"
        background_tasks.add_task(
            email_utils.send_verify_email, data.recipient, name
        )
    except BaseException:
        logger.error("Failed to send email", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email",
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
async def get_one_email_by_id(id: UUID4):
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
        message="Successfully fetched email", data=email
    )


# get template
@router.get("/templates/{name}", response_class=HTMLResponse)
async def get_email_template(request: Request, name: str):
    return templates.TemplateResponse(
        request=request,
        name="verify-email.html",
        context={"name": name},
    )
