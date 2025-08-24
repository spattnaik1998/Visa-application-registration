from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import BaseModel, EmailStr, validator
from typing import Literal, List, Optional
from datetime import datetime
import re
import io
import pytesseract
from PIL import Image
import cv2
import numpy as np
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

class DocumentUploadResponse(BaseModel):
    status: str
    message: str
    documents_processed: int
    validation_results: dict
    extracted_text: dict

# In-memory storage for demonstration (in production, use a database)
visa_applications = {}

# OCR and Computer Vision Helper Functions
def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract text from image using OCR"""
    try:
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Use pytesseract to extract text
        extracted_text = pytesseract.image_to_string(image, config='--psm 6')
        return extracted_text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract text from image: {str(e)}")

def detect_face_in_image(image_bytes: bytes) -> bool:
    """Detect if image contains a face using OpenCV"""
    try:
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("Could not decode image")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Load face cascade classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        return len(faces) > 0
    except Exception as e:
        raise ValueError(f"Failed to detect face in image: {str(e)}")

def validate_passport_number(extracted_text: str, expected_passport_number: str) -> bool:
    """Validate if passport number from OCR matches expected number"""
    # Remove spaces and convert to uppercase for comparison
    cleaned_extracted = re.sub(r'\s+', '', extracted_text.upper())
    cleaned_expected = re.sub(r'\s+', '', expected_passport_number.upper())
    
    # Check if expected passport number is found in extracted text
    return cleaned_expected in cleaned_extracted

def process_document(file_content: bytes, document_type: str, expected_passport_number: str = None) -> dict:
    """Process uploaded document with OCR and validation"""
    result = {
        "document_type": document_type,
        "extracted_text": "",
        "validation_passed": False,
        "validation_message": ""
    }
    
    try:
        if document_type == "photo":
            # For photos, check if face is detected
            has_face = detect_face_in_image(file_content)
            result["validation_passed"] = has_face
            result["validation_message"] = "Face detected in photo" if has_face else "No face detected in photo"
            result["extracted_text"] = "Photo validation complete"
            
        elif document_type == "passport":
            # For passport, extract text and validate passport number
            extracted_text = extract_text_from_image(file_content)
            result["extracted_text"] = extracted_text
            
            if expected_passport_number:
                passport_match = validate_passport_number(extracted_text, expected_passport_number)
                result["validation_passed"] = passport_match
                result["validation_message"] = (
                    f"Passport number {expected_passport_number} found in document" 
                    if passport_match 
                    else f"Passport number {expected_passport_number} not found in document"
                )
            else:
                result["validation_passed"] = bool(extracted_text)
                result["validation_message"] = "Text extracted from passport document"
                
        else:
            # For other documents, just extract text
            extracted_text = extract_text_from_image(file_content)
            result["extracted_text"] = extracted_text
            result["validation_passed"] = bool(extracted_text)
            result["validation_message"] = "Text successfully extracted from document"
            
    except Exception as e:
        result["validation_passed"] = False
        result["validation_message"] = f"Error processing document: {str(e)}"
        
    return result

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



@router.post("/upload_documents", response_model=DocumentUploadResponse)
async def upload_documents(
    application_id: str = Form(...),
    expected_passport_number: Optional[str] = Form(None),
    passport: Optional[UploadFile] = File(None),
    photo: Optional[UploadFile] = File(None),
    supporting_docs: Optional[List[UploadFile]] = File(None)
):
    """
    Upload and validate documents with OCR (Step 5).
    
    This endpoint handles document uploads with OCR processing and validation.
    """
    try:
        if not any([passport, photo, supporting_docs]):
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse(
                    status="error",
                    message="At least one document must be uploaded"
                ).dict()
            )
        
        # Create a new visa application instance for this step
        visa_app = VisaApplication()
        
        validation_results = {}
        extracted_text = {}
        uploaded_documents = {}
        documents_processed = 0
        
        # Process passport document
        if passport:
            try:
                file_content = await passport.read()
                result = process_document(file_content, "passport", expected_passport_number)
                validation_results["passport"] = result
                extracted_text["passport"] = result["extracted_text"]
                uploaded_documents["passport"] = {
                    "filename": passport.filename,
                    "content_type": passport.content_type,
                    "size": len(file_content)
                }
                documents_processed += 1
            except Exception as e:
                validation_results["passport"] = {
                    "document_type": "passport",
                    "validation_passed": False,
                    "validation_message": f"Failed to process passport: {str(e)}",
                    "extracted_text": ""
                }
        
        # Process photo
        if photo:
            try:
                file_content = await photo.read()
                result = process_document(file_content, "photo")
                validation_results["photo"] = result
                extracted_text["photo"] = result["extracted_text"]
                uploaded_documents["photo"] = {
                    "filename": photo.filename,
                    "content_type": photo.content_type,
                    "size": len(file_content)
                }
                documents_processed += 1
            except Exception as e:
                validation_results["photo"] = {
                    "document_type": "photo",
                    "validation_passed": False,
                    "validation_message": f"Failed to process photo: {str(e)}",
                    "extracted_text": ""
                }
        
        # Process supporting documents
        if supporting_docs:
            for i, doc in enumerate(supporting_docs):
                try:
                    file_content = await doc.read()
                    result = process_document(file_content, "supporting")
                    doc_key = f"supporting_doc_{i+1}"
                    validation_results[doc_key] = result
                    extracted_text[doc_key] = result["extracted_text"]
                    uploaded_documents[doc_key] = {
                        "filename": doc.filename,
                        "content_type": doc.content_type,
                        "size": len(file_content)
                    }
                    documents_processed += 1
                except Exception as e:
                    doc_key = f"supporting_doc_{i+1}"
                    validation_results[doc_key] = {
                        "document_type": "supporting",
                        "validation_passed": False,
                        "validation_message": f"Failed to process {doc.filename}: {str(e)}",
                        "extracted_text": ""
                    }
        
        # Store document data in visa application
        documents_data = {
            "uploaded_documents": uploaded_documents,
            "validation_results": validation_results,
            "extracted_text": extracted_text
        }
        
        message = visa_app.upload_documents(documents_data)
        
        # Check if any critical validations failed
        passport_failed = (passport and not validation_results.get("passport", {}).get("validation_passed", True))
        photo_failed = (photo and not validation_results.get("photo", {}).get("validation_passed", True))
        
        if passport_failed or photo_failed:
            failed_docs = []
            if passport_failed:
                failed_docs.append("passport validation")
            if photo_failed:
                failed_docs.append("photo validation")
            
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse(
                    status="error",
                    message=f"Document validation failed: {', '.join(failed_docs)}"
                ).dict()
            )
        
        # Store the application (in production, use database with proper session management)
        application_key = f"documents_{len(visa_applications) + 1}"
        visa_applications[application_key] = visa_app
        
        return {
            "status": "success",
            "message": "Documents uploaded and validated",
            "documents_processed": documents_processed,
            "validation_results": validation_results,
            "extracted_text": extracted_text
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                status="error", 
                message=f"Internal server error: {str(e)}"
            ).dict()
        )

