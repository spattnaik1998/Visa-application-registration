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

class PaymentRequest(BaseModel):
    application_id: str
    amount: float
    currency: Literal["USD", "EUR", "INR"]
    payment_method: Literal["credit_card", "debit_card", "upi", "paypal"]
    transaction_id: str
    
    @validator('application_id')
    def validate_application_id(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Application ID must be at least 3 characters long')
        if not re.match(r'^[A-Z0-9]+$', v.strip().upper()):
            raise ValueError('Application ID must be alphanumeric (letters and numbers only)')
        return v.strip().upper()
    
    @validator('amount')
    def validate_amount(cls, v):
        if not isinstance(v, (int, float)) or v <= 0:
            raise ValueError('Amount must be a positive number')
        if v < 50:
            raise ValueError('Minimum payment amount is 50')
        if v > 10000:  # Reasonable upper limit
            raise ValueError('Maximum payment amount is 10,000')
        return round(float(v), 2)  # Round to 2 decimal places
    
    @validator('transaction_id')
    def validate_transaction_id(cls, v):
        if not v or len(v.strip()) < 5:
            raise ValueError('Transaction ID must be at least 5 characters long')
        if not re.match(r'^[A-Z0-9]+$', v.strip().upper()):
            raise ValueError('Transaction ID must be alphanumeric (letters and numbers only)')
        return v.strip().upper()

class PaymentResponse(BaseModel):
    status: str
    message: str
    payment_confirmation_id: str
    amount: float
    currency: str

class InterviewScheduleRequest(BaseModel):
    application_id: str
    location: str
    date: str  # Format: YYYY-MM-DD
    
    @validator('application_id')
    def validate_application_id(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Application ID must be at least 3 characters long')
        if not re.match(r'^[A-Z0-9]+$', v.strip().upper()):
            raise ValueError('Application ID must be alphanumeric (letters and numbers only)')
        return v.strip().upper()
    
    @validator('location')
    def validate_location(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Location must be at least 2 characters long')
        return v.strip()
    
    @validator('date')
    def validate_date(cls, v):
        try:
            interview_date = datetime.strptime(v, '%Y-%m-%d')
            today = datetime.now()
            
            # Check if date is in the future
            if interview_date.date() <= today.date():
                raise ValueError('Interview date must be in the future')
                
            return v
        except ValueError as e:
            if "time data" in str(e):
                raise ValueError('Date must be in YYYY-MM-DD format')
            raise e

class InterviewScheduleResponse(BaseModel):
    status: str
    message: str
    interview_confirmation_id: str
    location: str
    date: str

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

@router.post("/pay_visa_fee", response_model=PaymentResponse)
async def pay_visa_fee(request: PaymentRequest):
    """
    Pay the visa application fee.
    
    This is Step 3 of the U.S. visa application process.
    """
    try:
        # Create a new visa application instance for this step
        visa_app = VisaApplication()
        
        # Prepare payment data
        payment_data = {
            "application_id": request.application_id,
            "amount": request.amount,
            "currency": request.currency,
            "payment_method": request.payment_method,
            "transaction_id": request.transaction_id
        }
        
        # Call the pay_fee method
        message = visa_app.pay_fee(payment_data)
        
        # Store the application (in production, use database with proper session management)
        application_id = f"payment_{len(visa_applications) + 1}"
        visa_applications[application_id] = visa_app
        
        return {
            "status": "success",
            "message": "Visa fee payment recorded successfully",
            "payment_confirmation_id": visa_app.payment_confirmation_id,
            "amount": request.amount,
            "currency": request.currency
        }
        
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

@router.post("/schedule_interview", response_model=InterviewScheduleResponse)
async def schedule_interview(request: InterviewScheduleRequest):
    """
    Schedule a visa interview (Step 4).
    
    This endpoint handles interview scheduling with location and date validation.
    """
    try:
        # Create a new visa application instance for this step
        visa_app = VisaApplication()
        
        # Prepare interview data
        interview_data = {
            "application_id": request.application_id,
            "location": request.location,
            "date": request.date
        }
        
        # Call the schedule_interview method
        message = visa_app.schedule_interview(interview_data)
        
        # Store the application (in production, use database with proper session management)
        application_id = f"interview_{len(visa_applications) + 1}"
        visa_applications[application_id] = visa_app
        
        return {
            "status": "success",
            "message": "Interview scheduled successfully",
            "interview_confirmation_id": visa_app.interview_confirmation_id,
            "location": request.location,
            "date": request.date
        }
        
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

