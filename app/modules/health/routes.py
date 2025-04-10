# app/features/health/routes.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["health"])


@router.get("/health", status_code=200)
async def health_check():
    """Simple health check endpoint for monitoring with Uptime Robot"""
    response = JSONResponse(content={"status": "healthy"})
    # Add CORS headers directly since this is a simple endpoint
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, HEAD, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response
