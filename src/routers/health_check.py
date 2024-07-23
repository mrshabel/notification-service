from fastapi import APIRouter

router = APIRouter(prefix="/health-check")

@router.get("")
async def health_check():
    """Checks whether the application is healthy to process requests
    """
    return "Great! Notification service is healthy"