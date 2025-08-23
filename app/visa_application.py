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
    
    def gather_documents(self, documents):
        """Gather required documents for the visa application"""
        if self.visa_type is None:
            raise ValueError("No visa type selected. Please select a visa type first.")
        
        if not documents or not isinstance(documents, dict):
            raise ValueError("Documents must be provided as a non-empty dictionary")
        
        self.documents = documents.copy()
        
        required_documents = {
            "B1/B2": ["passport"],
            "F1": ["passport", "admission_letter"],
            "H1B": ["passport", "job_offer"],
            "J1": ["passport", "sponsor_letter"]
        }
        
        required_for_visa = required_documents.get(self.visa_type, [])
        missing_documents = []
        
        for doc in required_for_visa:
            if doc not in documents or not documents[doc]:
                missing_documents.append(doc)
        
        if missing_documents:
            missing_list = ", ".join(missing_documents)
            raise ValueError(f"Missing required documents for {self.visa_type} visa: {missing_list}")
        
        return f"All required documents gathered for {self.visa_type} visa"
    
    def fill_ds160(self, form_data):
        """Fill out the DS-160 online application form"""
        import random
        import string
        
        if self.visa_type is None:
            raise ValueError("No visa type selected. Please select a visa type first.")
        
        if not form_data or not isinstance(form_data, dict):
            raise ValueError("Form data must be provided as a non-empty dictionary")
        
        required_fields = ["full_name", "dob", "passport_number", "nationality", "travel_purpose"]
        missing_fields = []
        
        for field in required_fields:
            if field not in form_data:
                missing_fields.append(field)
            elif not isinstance(form_data[field], str) or not form_data[field].strip():
                if field not in missing_fields:
                    missing_fields.append(field)
        
        if missing_fields:
            missing_list = ", ".join(missing_fields)
            raise ValueError(f"Missing or invalid required fields: {missing_list}")
        
        self.ds160_form_data = form_data.copy()
        
        self.ds160_confirmation_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        return f"DS-160 form submitted successfully. Confirmation ID: {self.ds160_confirmation_id}"
    
    def pay_fee(self, amount):
        """Pay the visa application fee"""
        import random
        import string
        
        if self.visa_type is None:
            raise ValueError("No visa type selected. Please select a visa type first.")
        
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Payment amount must be a non-negative number")
        
        visa_fees = {
            "B1/B2": 160.0,
            "F1": 160.0,
            "H1B": 190.0,
            "J1": 160.0
        }
        
        required_fee = visa_fees.get(self.visa_type)
        
        if amount < required_fee:
            raise ValueError(f"Insufficient payment. Required fee for {self.visa_type} visa is ${required_fee:.2f}, but ${amount:.2f} was provided")
        
        self.payment_amount = amount
        self.payment_confirmation_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        return f"Payment successful. Amount: ${amount:.2f}, Confirmation ID: {self.payment_confirmation_id}"
    
    def schedule_appointment(self, appointment_date, appointment_time=None):
        """Schedule an appointment at the U.S. embassy or consulate"""
        from datetime import datetime
        
        if self.payment_confirmation_id is None:
            raise ValueError("Payment must be completed before scheduling an appointment")
        
        if not appointment_date or not isinstance(appointment_date, str):
            raise ValueError("Appointment date must be provided as a non-empty string")
        
        try:
            date_obj = datetime.strptime(appointment_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD format")
        
        today = datetime.now().date()
        if date_obj.date() <= today:
            raise ValueError("Appointment date must be in the future")
        
        appointment_info = {
            "date": appointment_date,
            "time": appointment_time if appointment_time else "09:00",
            "location": "U.S. Embassy/Consulate"
        }
        
        self.appointment = appointment_info
        
        time_display = f" at {appointment_info['time']}" if appointment_time else ""
        return f"Appointment scheduled successfully for {appointment_date}{time_display} at {appointment_info['location']}"
    
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