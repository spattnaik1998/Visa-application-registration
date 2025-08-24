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