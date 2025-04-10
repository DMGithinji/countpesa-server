import logging

from fastapi import FastAPI

from app.config import settings
from app.middleware import setup_middleware
from app.modules.feedback.routes import router as feedback_router
from app.modules.health.routes import router as health_router
from app.modules.mpesa_statement_parser.routes import router as pdf_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="A simple service for processing PDF statements and collecting feedback",
    version="1.0.0",
    debug=settings.DEBUG,
)

setup_middleware(app)

app.include_router(feedback_router)
app.include_router(pdf_router)
app.include_router(health_router)


@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting up {settings.APP_NAME}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}")
