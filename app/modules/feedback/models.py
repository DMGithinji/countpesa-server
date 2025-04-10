from typing import Optional

from pydantic import BaseModel, Field


class FeedbackRequest(BaseModel):
    google_sheet_name: str = Field(
        ...,
        description="Name of the Google Sheet to store the feedback",
        example="Countpesa Web App Feedback",
    )
    message: str = Field(
        ...,
        description="Feedback message content",
        example="I really like the new bank statement parsing feature!",
    )
    type: Optional[str] = Field(
        None,
        description="Type of feedback (e.g., bug, feature request, comment)",
        example="feature_request",
    )
    email: Optional[str] = Field(
        None, description="Email of the person providing feedback", example="user@example.com"
    )

    class Config:
        schema_extra = {
            "example": {
                "google_sheet_name": "Countpesa Web App Feedback",
                "message": "Would love to see support for Equity Bank!",
                "type": "suggestion",
                "email": "user@example.com",
            }
        }


class FeedbackResponse(BaseModel):
    status: str = Field(..., description="Response status (success or error)", example="success")
    message: str = Field(
        ..., description="Response message", example="Feedback submitted successfully"
    )

    class Config:
        schema_extra = {
            "example": {"status": "success", "message": "Feedback submitted successfully"}
        }
