class VisaApplication:
    """
    A class to simulate the U.S. visa application process step by step.
    """
    
    def __init__(self):
        self.visa_type = None
        self.admission_letter = False
        self.job_offer = False
        self.sponsor_letter = False
    
    def select_visa_type(self, visa_type):
        """Select the appropriate visa type (B-1/B-2, F-1, H-1B, etc.)"""
        valid_visa_types = ["B1/B2", "F1", "H1B", "J1"]
        
        if not visa_type or not isinstance(visa_type, str):
            raise ValueError("Visa type must be a non-empty string")
        
        if visa_type not in valid_visa_types:
            raise ValueError(f"Invalid visa type '{visa_type}'. Valid types are: {', '.join(valid_visa_types)}")
        
        self.visa_type = visa_type
        return f"Visa type '{visa_type}' selected successfully"
    
    def check_eligibility(self, admission_letter=None, job_offer=None, sponsor_letter=None):
        """Check eligibility requirements for the selected visa type"""
        if self.visa_type is None:
            raise ValueError("No visa type selected. Please select a visa type first.")
        
        if admission_letter is not None:
            self.admission_letter = admission_letter
        if job_offer is not None:
            self.job_offer = job_offer
        if sponsor_letter is not None:
            self.sponsor_letter = sponsor_letter
        
        if self.visa_type == "B1/B2":
            return "Eligibility confirmed for B1/B2 visa"
        
        elif self.visa_type == "F1":
            if not self.admission_letter:
                raise ValueError("F1 visa requires an admission letter from a U.S. educational institution")
            return "Eligibility confirmed for F1 visa with admission letter"
        
        elif self.visa_type == "H1B":
            if not self.job_offer:
                raise ValueError("H1B visa requires a job offer from a U.S. employer")
            return "Eligibility confirmed for H1B visa with job offer"
        
        elif self.visa_type == "J1":
            if not self.sponsor_letter:
                raise ValueError("J1 visa requires a sponsor letter from an approved program sponsor")
            return "Eligibility confirmed for J1 visa with sponsor letter"
    
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