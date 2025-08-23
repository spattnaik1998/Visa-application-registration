from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, validator
from typing import Literal
from datetime import datetime
import re
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

class DS160FormRequest(BaseModel):
    full_name: str
    passport_number: str
    dob: str  # Format: YYYY-MM-DD
    nationality: str
    email: EmailStr
    
    @validator('full_name')
    def validate_full_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Full name must be at least 2 characters long')
        if not re.match(r'^[a-zA-Z\s\-\'\.]+$', v.strip()):
            raise ValueError('Full name can only contain letters, spaces, hyphens, apostrophes, and periods')
        return v.strip()
    
    @validator('passport_number')
    def validate_passport_number(cls, v):
        if not v or len(v.strip()) < 6:
            raise ValueError('Passport number must be at least 6 characters long')
        if not re.match(r'^[A-Z0-9]+$', v.strip().upper()):
            raise ValueError('Passport number must be alphanumeric (letters and numbers only)')
        return v.strip().upper()
    
    @validator('dob')
    def validate_dob(cls, v):
        try:
            dob_date = datetime.strptime(v, '%Y-%m-%d')
            today = datetime.now()
            
            # Check if date is in the past
            if dob_date.date() >= today.date():
                raise ValueError('Date of birth must be in the past')
            
            # Check minimum age (e.g., must be at least 1 year old)
            age_years = (today - dob_date).days / 365.25
            if age_years < 1:
                raise ValueError('Invalid date of birth')
                
            # Check maximum age (reasonable limit)
            if age_years > 120:
                raise ValueError('Invalid date of birth')
                
            return v
        except ValueError as e:
            if "time data" in str(e):
                raise ValueError('Date of birth must be in YYYY-MM-DD format')
            raise e
    
    @validator('nationality')
    def validate_nationality(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Nationality must be at least 2 characters long')
        if not re.match(r'^[a-zA-Z\s]+$', v.strip()):
            raise ValueError('Nationality can only contain letters and spaces')
        return v.strip().title()

class DS160FormResponse(BaseModel):
    status: str
    message: str
    confirmation_id: str

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

@router.post("/fill_ds160", response_model=DS160FormResponse)
async def fill_ds160(request: DS160FormRequest):
    """
    Fill out the DS-160 form.
    
    This is Step 2 of the U.S. visa application process.
    """
    try:
        # Create a new visa application instance for this step
        visa_app = VisaApplication()
        
        # Prepare form data
        form_data = {
            "full_name": request.full_name,
            "passport_number": request.passport_number,
            "dob": request.dob,
            "nationality": request.nationality,
            "email": request.email
        }
        
        # Call the fill_ds160 method
        message = visa_app.fill_ds160(form_data)
        
        # Store the application (in production, use database with proper session management)
        application_id = f"ds160_{len(visa_applications) + 1}"
        visa_applications[application_id] = visa_app
        
        return DS160FormResponse(
            status="success",
            message="DS-160 form submitted successfully",
            confirmation_id=visa_app.ds160_confirmation_id
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