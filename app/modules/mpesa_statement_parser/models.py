from typing import List, Optional

from pydantic import BaseModel, Field


class PDFStatementRequest(BaseModel):
    password: str

    class Config:
        schema_extra = {"example": {"password": "required_pdf_password"}}


class TransactionModel(BaseModel):
    code: str = Field(..., description="Transaction code")
    date: int = Field(..., description="Transaction timestamp in milliseconds since epoch")
    description: str = Field(..., description="Original transaction description")
    status: str = Field(..., description="Transaction status")
    amount: float = Field(..., description="Transaction amount")
    balance: float = Field(..., description="Account balance after transaction")
    account: str = Field(..., description="Account involved in the transaction")
    type: str = Field(..., description="Transaction type (e.g., Till Number, Paybill, Send Money)")
    category: Optional[str] = Field(None, description="Optional transaction category")

    class Config:
        schema_extra = {
            "example": {
                "code": "QER7OI9RZD",
                "date": 1617235200000,  # 2021-04-01 00:00:00
                "description": "Pay Bill to KPLC - 888880",
                "status": "Completed",
                "amount": 1000.0,
                "balance": 5000.0,
                "account": "KPLC - 888880",
                "type": "Paybill",
                "category": "",
            }
        }


class StatementResponseModel(BaseModel):
    transactions: List[TransactionModel] = Field(..., description="List of parsed transactions")


class APIResponseModel(BaseModel):
    status: str = Field(..., description="Response status (success or error)")
    data: StatementResponseModel = Field(..., description="Parsed statement data")
    message: str = Field(..., description="Response message")

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "transactions": [
                        {
                            "code": "QER7OI9RZD",
                            "date": 1617235200000,
                            "description": "Pay Bill to KPLC - 888880",
                            "status": "Completed",
                            "amount": 1000.0,
                            "balance": 5000.0,
                            "account": "KPLC - 888880",
                            "type": "Paybill",
                            "category": "",
                        }
                    ]
                },
                "message": "Successfully processed 1 transactions",
            }
        }
