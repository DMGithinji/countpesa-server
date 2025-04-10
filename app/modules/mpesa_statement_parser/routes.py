import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from .models import APIResponseModel, StatementResponseModel
from .utils import get_parsed_statement

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/process-mpesa-statement", tags=["pdf"])
logger = logging.getLogger(__name__)


@router.post(
    "/",
    status_code=200,
    response_model=APIResponseModel,
    summary="Process MPESA PDF Statement",
    description="Upload and process an MPESA PDF statement. Extracts all transactions.",
)
async def process_pdf(
    statement: UploadFile = File(..., description="MPESA PDF statement file"),
    password: str = Form(..., description="PDF password (usually your phone number)"),
):
    try:
        if not statement.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        parsed_statement = get_parsed_statement(statement.file, password)
        transactions = parsed_statement.get("transactions", [])
        response_data = StatementResponseModel(transactions=transactions)

        return APIResponseModel(
            status="success",
            data=response_data,
            message=f"Successfully processed {len(transactions)} transactions",
        )
    except ValueError as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error processing PDF: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in PDF processing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {str(e)}")
