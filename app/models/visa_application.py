class VisaApplication:
    """
    A class to simulate the U.S. visa application process step by step.
    """
    
    def __init__(self):
        self.visa_type = None
        self.admission_letter = False
        self.job_offer = False
        self.sponsor_letter = False
        self.documents = {}
        self.ds160_form_data = {}
        self.ds160_confirmation_id = None
        self.payment_amount = 0.0
        self.payment_confirmation_id = None
        self.appointment = None
        self.biometrics_confirmation_id = None
        self.interview_result = None
        self.processing_status = None
        self.visa_number = None
        
        # DS-160 specific fields
        self.full_name = None
        self.passport_number = None
        self.dob = None
        self.nationality = None
        self.email = None
        
        # Payment specific fields
        self.fee_amount = None
        self.fee_currency = None
        self.payment_method = None
        self.transaction_id = None
        self.payment_status = None
        self.payment_data = {}
        
        # Interview specific fields
        self.interview_location = None
        self.interview_date = None
        self.interview_confirmation_id = None
        self.interview_data = {}
        
        # Document specific fields
        self.uploaded_documents = {}
        self.document_validation_results = {}
        self.extracted_text = {}
        
        # Interview attendance specific fields
        self.interview_attendance_status = None
        self.interview_attended = False
        self.attendance_data = {}
    
    def select_visa_type(self, visa_type):
        """Select the appropriate visa type (B-1/B-2, F-1, H-1B, etc.)"""
        valid_visa_types = ["B1/B2", "F1", "H1B", "J1"]
        
        if not visa_type or not isinstance(visa_type, str):
            raise ValueError("Visa type must be a non-empty string")
        
        if visa_type not in valid_visa_types:
            raise ValueError(f"Invalid visa type '{visa_type}'. Valid types are: {', '.join(valid_visa_types)}")
        
        self.visa_type = visa_type
        return f"Visa type '{visa_type}' selected successfully"
    
    def check_eligibility(self):
        """Check eligibility requirements for the selected visa type"""
        pass
    
    def gather_documents(self):
        """Gather required documents for the visa application"""
        pass
    
    def fill_ds160(self, form_data: dict):
        """Fill out the DS-160 online application form"""
        import random
        import string
        
        # Store form data
        self.full_name = form_data.get("full_name")
        self.passport_number = form_data.get("passport_number")
        self.dob = form_data.get("dob")
        self.nationality = form_data.get("nationality")
        self.email = form_data.get("email")
        
        # Store in ds160_form_data for backward compatibility
        self.ds160_form_data = form_data.copy()
        
        # Generate DS-160 confirmation ID
        if not self.ds160_confirmation_id:
            self.ds160_confirmation_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        return f"DS-160 form submitted successfully. Confirmation ID: {self.ds160_confirmation_id}"
    
    def pay_fee(self, payment_data: dict):
        """Pay the visa application fee"""
        import random
        import string
        
        # Store payment data
        self.payment_data = payment_data.copy()
        self.fee_amount = payment_data.get("amount")
        self.fee_currency = payment_data.get("currency")
        self.payment_method = payment_data.get("payment_method")
        self.transaction_id = payment_data.get("transaction_id")
        self.payment_status = "completed"
        
        # Generate payment confirmation ID if not already exists
        if not self.payment_confirmation_id:
            self.payment_confirmation_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        return f"Visa fee payment of {self.fee_amount} {self.fee_currency} processed successfully. Payment ID: {self.payment_confirmation_id}"
    
    def schedule_interview(self, interview_data: dict):
        """Schedule a visa interview at the U.S. embassy or consulate"""
        import random
        import string
        
        # Store interview data
        self.interview_data = interview_data.copy()
        self.interview_location = interview_data.get("location")
        self.interview_date = interview_data.get("date")
        
        # Generate interview confirmation ID if not already exists
        if not self.interview_confirmation_id:
            self.interview_confirmation_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        return f"Interview scheduled successfully for {self.interview_date} at {self.interview_location}. Confirmation ID: {self.interview_confirmation_id}"
    
    def upload_documents(self, documents_data: dict):
        """Upload and store document validation results"""
        # Store all document information
        self.uploaded_documents = documents_data.get("uploaded_documents", {})
        self.document_validation_results = documents_data.get("validation_results", {})
        self.extracted_text = documents_data.get("extracted_text", {})
        
        # Count successful validations
        successful_validations = sum(1 for result in self.document_validation_results.values() 
                                   if result.get("validation_passed", False))
        total_documents = len(self.document_validation_results)
        
        return f"Documents uploaded and validated: {successful_validations}/{total_documents} validations passed"
    
    def attend_interview(self, attendance_data: dict):
        """Mark interview attendance status"""
        # Store attendance information
        self.attendance_data = attendance_data.copy()
        self.interview_attendance_status = attendance_data.get("status")
        self.interview_attended = (attendance_data.get("status") == "attended")
        
        if self.interview_attended:
            return f"Interview attendance marked as 'attended' for application {attendance_data.get('application_id', 'N/A')}"
        else:
            return f"Interview attendance marked as 'missed' for application {attendance_data.get('application_id', 'N/A')}"
    
    def schedule_appointment(self):
        """Schedule an appointment at the U.S. embassy or consulate"""
        pass
    
    def collect_biometrics(self):
        """Collect biometric information (fingerprints, photo)"""
        pass
    
    def interview(self):
        """Attend the visa interview"""
        pass
    
    def process_application(self):
        """Administrative processing of the visa application"""
        pass
    
    def issue_visa(self):
        """Final visa issuance or denial"""
        pass