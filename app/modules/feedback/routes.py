import logging

from fastapi import APIRouter, HTTPException

from .g_sheets import post_feedback_data
from .models import FeedbackRequest, FeedbackResponse

router = APIRouter(prefix="/feedback", tags=["feedback"])
logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=FeedbackResponse,
    status_code=200,
    summary="Submit User Feedback",
    description="Submit user feedback to be stored in a specified Google Sheet.",
)
async def submit_feedback_handler(feedback: FeedbackRequest):
    try:
        post_feedback_data(feedback.model_dump())
        return FeedbackResponse(status="success", message="Feedback submitted successfully")
    except Exception:
        logger.exception("Failed to submit feedback to Google Sheets")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")
