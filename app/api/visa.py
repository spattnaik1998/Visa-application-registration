from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from app.models.visa_application import VisaApplication

router = APIRouter()

# Pydantic models for request/response
class VisaTypeRequest(BaseModel):
    visa_type: Literal["B1/B2", "F1", "H1B", "J1"]

class VisaTypeResponse(BaseModel):
    status: str
    message: str
    visa_type: str

class ErrorResponse(BaseModel):
    status: str
    message: str

# In-memory storage for demonstration (in production, use a database)
visa_applications = {}

@router.post("/select_visa_type", response_model=VisaTypeResponse)
async def select_visa_type(request: VisaTypeRequest):
    """
    Select a visa type for the application.
    
    This is Step 1 of the U.S. visa application process.
    """
    try:
        # Create a new visa application instance
        visa_app = VisaApplication()
        
        # Call the select_visa_type method
        message = visa_app.select_visa_type(request.visa_type)
        
        # Store the application (in production, use database with proper session management)
        application_id = f"app_{len(visa_applications) + 1}"
        visa_applications[application_id] = visa_app
        
        return VisaTypeResponse(
            status="success",
            message=message,
            visa_type=request.visa_type
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                status="error",
                message=str(e)
            ).dict()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                status="error", 
                message="Internal server error"
            ).dict()
        )

@router.get("/visa_types")
async def get_visa_types():
    """Get the list of available visa types"""
    return {
        "visa_types": ["B1/B2", "F1", "H1B", "J1"],
        "descriptions": {
            "B1/B2": "Business/Tourism visa",
            "F1": "Student visa",
            "H1B": "Specialty occupation worker visa", 
            "J1": "Exchange visitor visa"
        }
    }