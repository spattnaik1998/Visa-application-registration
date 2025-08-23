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
    
    def fill_ds160(self):
        """Fill out the DS-160 online application form"""
        pass
    
    def pay_fee(self):
        """Pay the visa application fee"""
        pass
    
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