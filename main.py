from typing import Optional
import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from g_sheets import post_feedback_data
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
      "https://justtldr.com",
      "chrome-extension://cmnjpgpkkdmkkmpliipnmhbelgbiefpa",
      "http://localhost:3000",
      ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class FeedbackRequest(BaseModel):
    google_sheet: str
    message: str
    type: Optional[str] = None
    email: Optional[str] = None

@app.post("/feedback/")
async def submit_feedback(feedback: FeedbackRequest, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(post_feedback_data, feedback.dict())
        return {"status": "success", "message": "Feedback submitted successfully"}
    except Exception as e:
        logger.error(f"Unexpected error in feedback submission: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")

@app.get("/health")
async def health_check():
    response = JSONResponse(content={"status": "healthy"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response