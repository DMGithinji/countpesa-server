import asyncio
from typing import Optional
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from g_sheets import post_feedback_data

app = FastAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class FeedbackRequest(BaseModel):
    google_sheet: str
    message: str
    type: Optional[str] = None
    email: Optional[str] = None

@app.post("/feedback/")
async def submit_feedback(feedback: FeedbackRequest):
    try:
        asyncio.create_task(post_feedback_data(feedback.dict()))
        return {"status": "success", "message": "Feedback submitted successfully"}
    except Exception as e:
        logger.error(f"Unexpected error in feedback submission: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}