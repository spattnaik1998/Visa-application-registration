import pytest
from app.visa_application import VisaApplication


class TestVisaApplication:
    """Test suite for VisaApplication class"""
    
    @pytest.fixture
    def visa_app(self):
        """Fixture to create a VisaApplication instance"""
        return VisaApplication()
    
    def test_select_visa_type_valid_b1b2(self, visa_app):
        """Test valid B1/B2 visa type selection"""
        result = visa_app.select_visa_type("B1/B2")
        assert visa_app.visa_type == "B1/B2"
        assert result == "Visa type 'B1/B2' selected successfully"
    
    def test_select_visa_type_valid_f1(self, visa_app):
        """Test valid F1 visa type selection"""
        result = visa_app.select_visa_type("F1")
        assert visa_app.visa_type == "F1"
        assert result == "Visa type 'F1' selected successfully"
    
    def test_select_visa_type_invalid(self, visa_app):
        """Test invalid visa type raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            visa_app.select_visa_type("Tourist")
        assert "Invalid visa type 'Tourist'" in str(exc_info.value)
        assert visa_app.visa_type is None
    
    def test_select_visa_type_empty_string(self, visa_app):
        """Test empty string raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            visa_app.select_visa_type("")
        assert "Visa type must be a non-empty string" in str(exc_info.value)
        assert visa_app.visa_type is None
    
    def test_check_eligibility_f1_with_admission_letter(self, visa_app):
        """Test F1 eligibility with admission letter"""
        visa_app.select_visa_type("F1")
        result = visa_app.check_eligibility(admission_letter=True)
        assert result == "Eligibility confirmed for F1 visa with admission letter"
    
    def test_check_eligibility_f1_without_admission_letter(self, visa_app):
        """Test F1 eligibility without admission letter raises ValueError"""
        visa_app.select_visa_type("F1")
        with pytest.raises(ValueError) as exc_info:
            visa_app.check_eligibility(admission_letter=False)
        assert "F1 visa requires an admission letter" in str(exc_info.value)
    
    def test_check_eligibility_b1b2_automatic_pass(self, visa_app):
        """Test B1/B2 eligibility passes automatically"""
        visa_app.select_visa_type("B1/B2")
        result = visa_app.check_eligibility()
        assert result == "Eligibility confirmed for B1/B2 visa"
    
    def test_check_eligibility_h1b_with_job_offer(self, visa_app):
        """Test H1B eligibility with job offer"""
        visa_app.select_visa_type("H1B")
        result = visa_app.check_eligibility(job_offer=True)
        assert result == "Eligibility confirmed for H1B visa with job offer"
    
    def test_check_eligibility_h1b_without_job_offer(self, visa_app):
        """Test H1B eligibility without job offer raises ValueError"""
        visa_app.select_visa_type("H1B")
        with pytest.raises(ValueError) as exc_info:
            visa_app.check_eligibility(job_offer=False)
        assert "H1B visa requires a job offer" in str(exc_info.value)
    
    def test_check_eligibility_j1_with_sponsor_letter(self, visa_app):
        """Test J1 eligibility with sponsor letter"""
        visa_app.select_visa_type("J1")
        result = visa_app.check_eligibility(sponsor_letter=True)
        assert result == "Eligibility confirmed for J1 visa with sponsor letter"
    
    def test_check_eligibility_j1_without_sponsor_letter(self, visa_app):
        """Test J1 eligibility without sponsor letter raises ValueError"""
        visa_app.select_visa_type("J1")
        with pytest.raises(ValueError) as exc_info:
            visa_app.check_eligibility(sponsor_letter=False)
        assert "J1 visa requires a sponsor letter" in str(exc_info.value)
    
    def test_check_eligibility_no_visa_type_selected(self, visa_app):
        """Test check eligibility without selecting visa type raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            visa_app.check_eligibility()
        assert "No visa type selected" in str(exc_info.value)
    
    def test_gather_documents_b1b2_valid(self, visa_app):
        """Test B1/B2 visa document gathering with valid documents"""
        visa_app.select_visa_type("B1/B2")
        documents = {"passport": True}
        result = visa_app.gather_documents(documents)
        assert result == "All required documents gathered for B1/B2 visa"
        assert visa_app.documents == documents
    
    def test_gather_documents_f1_valid(self, visa_app):
        """Test F1 visa document gathering with valid documents"""
        visa_app.select_visa_type("F1")
        documents = {"passport": True, "admission_letter": True}
        result = visa_app.gather_documents(documents)
        assert result == "All required documents gathered for F1 visa"
        assert visa_app.documents == documents
    
    def test_gather_documents_h1b_valid(self, visa_app):
        """Test H1B visa document gathering with valid documents"""
        visa_app.select_visa_type("H1B")
        documents = {"passport": True, "job_offer": True}
        result = visa_app.gather_documents(documents)
        assert result == "All required documents gathered for H1B visa"
        assert visa_app.documents == documents
    
    def test_gather_documents_j1_valid(self, visa_app):
        """Test J1 visa document gathering with valid documents"""
        visa_app.select_visa_type("J1")
        documents = {"passport": True, "sponsor_letter": True}
        result = visa_app.gather_documents(documents)
        assert result == "All required documents gathered for J1 visa"
        assert visa_app.documents == documents
    
    def test_gather_documents_f1_missing_admission_letter(self, visa_app):
        """Test F1 visa with missing admission letter"""
        visa_app.select_visa_type("F1")
        documents = {"passport": True, "admission_letter": False}
        with pytest.raises(ValueError) as exc_info:
            visa_app.gather_documents(documents)
        assert "Missing required documents for F1 visa: admission_letter" in str(exc_info.value)
    
    def test_gather_documents_h1b_missing_job_offer(self, visa_app):
        """Test H1B visa with missing job offer"""
        visa_app.select_visa_type("H1B")
        documents = {"passport": True}
        with pytest.raises(ValueError) as exc_info:
            visa_app.gather_documents(documents)
        assert "Missing required documents for H1B visa: job_offer" in str(exc_info.value)
    
    def test_gather_documents_missing_passport(self, visa_app):
        """Test any visa with missing passport"""
        visa_app.select_visa_type("B1/B2")
        documents = {"passport": False}
        with pytest.raises(ValueError) as exc_info:
            visa_app.gather_documents(documents)
        assert "Missing required documents for B1/B2 visa: passport" in str(exc_info.value)
    
    def test_gather_documents_empty_dictionary(self, visa_app):
        """Test gather documents with empty dictionary"""
        visa_app.select_visa_type("B1/B2")
        with pytest.raises(ValueError) as exc_info:
            visa_app.gather_documents({})
        assert "Documents must be provided as a non-empty dictionary" in str(exc_info.value)
    
    def test_gather_documents_no_visa_type_selected(self, visa_app):
        """Test gather documents without selecting visa type"""
        documents = {"passport": True}
        with pytest.raises(ValueError) as exc_info:
            visa_app.gather_documents(documents)
        assert "No visa type selected" in str(exc_info.value)
    
    def test_fill_ds160_valid_form(self, visa_app):
        """Test DS-160 form filling with valid data"""
        visa_app.select_visa_type("B1/B2")
        form_data = {
            "full_name": "John Doe",
            "dob": "1990-01-01",
            "passport_number": "A12345678",
            "nationality": "India",
            "travel_purpose": "Tourism"
        }
        result = visa_app.fill_ds160(form_data)
        assert "DS-160 form submitted successfully" in result
        assert "Confirmation ID:" in result
        assert visa_app.ds160_confirmation_id is not None
        assert len(visa_app.ds160_confirmation_id) == 8
        assert visa_app.ds160_form_data == form_data
    
    def test_fill_ds160_missing_required_fields(self, visa_app):
        """Test DS-160 form with missing required fields"""
        visa_app.select_visa_type("B1/B2")
        form_data = {
            "full_name": "John Doe",
            "dob": "1990-01-01"
        }
        with pytest.raises(ValueError) as exc_info:
            visa_app.fill_ds160(form_data)
        assert "Missing or invalid required fields:" in str(exc_info.value)
        assert "passport_number" in str(exc_info.value)
        assert "nationality" in str(exc_info.value)
        assert "travel_purpose" in str(exc_info.value)
    
    def test_fill_ds160_empty_dictionary(self, visa_app):
        """Test DS-160 form with empty dictionary"""
        visa_app.select_visa_type("B1/B2")
        with pytest.raises(ValueError) as exc_info:
            visa_app.fill_ds160({})
        assert "Form data must be provided as a non-empty dictionary" in str(exc_info.value)
    
    def test_fill_ds160_invalid_data_types(self, visa_app):
        """Test DS-160 form with invalid data types"""
        visa_app.select_visa_type("B1/B2")
        form_data = {
            "full_name": 12345,
            "dob": "1990-01-01",
            "passport_number": "A12345678",
            "nationality": "India",
            "travel_purpose": "Tourism"
        }
        with pytest.raises(ValueError) as exc_info:
            visa_app.fill_ds160(form_data)
        assert "Missing or invalid required fields: full_name" in str(exc_info.value)
    
    def test_fill_ds160_empty_string_fields(self, visa_app):
        """Test DS-160 form with empty string fields"""
        visa_app.select_visa_type("B1/B2")
        form_data = {
            "full_name": "",
            "dob": "1990-01-01",
            "passport_number": "A12345678",
            "nationality": "India",
            "travel_purpose": "Tourism"
        }
        with pytest.raises(ValueError) as exc_info:
            visa_app.fill_ds160(form_data)
        assert "Missing or invalid required fields: full_name" in str(exc_info.value)
    
    def test_fill_ds160_no_visa_type_selected(self, visa_app):
        """Test DS-160 form without selecting visa type"""
        form_data = {
            "full_name": "John Doe",
            "dob": "1990-01-01",
            "passport_number": "A12345678",
            "nationality": "India",
            "travel_purpose": "Tourism"
        }
        with pytest.raises(ValueError) as exc_info:
            visa_app.fill_ds160(form_data)
        assert "No visa type selected" in str(exc_info.value)
    
    def test_pay_fee_exact_amount_b1b2(self, visa_app):
        """Test exact fee payment for B1/B2 visa"""
        visa_app.select_visa_type("B1/B2")
        result = visa_app.pay_fee(160.0)
        assert "Payment successful" in result
        assert "Amount: $160.00" in result
        assert "Confirmation ID:" in result
        assert visa_app.payment_confirmation_id is not None
        assert len(visa_app.payment_confirmation_id) == 8
        assert visa_app.payment_amount == 160.0
    
    def test_pay_fee_exact_amount_h1b(self, visa_app):
        """Test exact fee payment for H1B visa"""
        visa_app.select_visa_type("H1B")
        result = visa_app.pay_fee(190.0)
        assert "Payment successful" in result
        assert "Amount: $190.00" in result
        assert "Confirmation ID:" in result
        assert visa_app.payment_confirmation_id is not None
        assert visa_app.payment_amount == 190.0
    
    def test_pay_fee_overpayment(self, visa_app):
        """Test overpayment should be accepted"""
        visa_app.select_visa_type("F1")
        result = visa_app.pay_fee(200.0)
        assert "Payment successful" in result
        assert "Amount: $200.00" in result
        assert "Confirmation ID:" in result
        assert visa_app.payment_confirmation_id is not None
        assert visa_app.payment_amount == 200.0
    
    def test_pay_fee_underpayment_b1b2(self, visa_app):
        """Test underpayment for B1/B2 visa should raise ValueError"""
        visa_app.select_visa_type("B1/B2")
        with pytest.raises(ValueError) as exc_info:
            visa_app.pay_fee(100.0)
        assert "Insufficient payment" in str(exc_info.value)
        assert "Required fee for B1/B2 visa is $160.00" in str(exc_info.value)
        assert "$100.00 was provided" in str(exc_info.value)
    
    def test_pay_fee_underpayment_h1b(self, visa_app):
        """Test underpayment for H1B visa should raise ValueError"""
        visa_app.select_visa_type("H1B")
        with pytest.raises(ValueError) as exc_info:
            visa_app.pay_fee(150.0)
        assert "Insufficient payment" in str(exc_info.value)
        assert "Required fee for H1B visa is $190.00" in str(exc_info.value)
        assert "$150.00 was provided" in str(exc_info.value)
    
    def test_pay_fee_negative_amount(self, visa_app):
        """Test negative payment amount should raise ValueError"""
        visa_app.select_visa_type("B1/B2")
        with pytest.raises(ValueError) as exc_info:
            visa_app.pay_fee(-50.0)
        assert "Payment amount must be a non-negative number" in str(exc_info.value)
    
    def test_pay_fee_no_visa_type_selected(self, visa_app):
        """Test payment without selecting visa type should raise ValueError"""
        with pytest.raises(ValueError) as exc_info:
            visa_app.pay_fee(160.0)
        assert "No visa type selected" in str(exc_info.value)
    
    def test_schedule_appointment_valid_future_date(self, visa_app):
        """Test scheduling appointment with valid future date"""
        from datetime import datetime, timedelta
        
        visa_app.select_visa_type("B1/B2")
        visa_app.pay_fee(160.0)
        
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        result = visa_app.schedule_appointment(future_date)
        
        assert "Appointment scheduled successfully" in result
        assert future_date in result
        assert "U.S. Embassy/Consulate" in result
        assert visa_app.appointment is not None
        assert visa_app.appointment["date"] == future_date
        assert visa_app.appointment["time"] == "09:00"
        assert visa_app.appointment["location"] == "U.S. Embassy/Consulate"
    
    def test_schedule_appointment_with_time(self, visa_app):
        """Test scheduling appointment with specific time"""
        from datetime import datetime, timedelta
        
        visa_app.select_visa_type("F1")
        visa_app.pay_fee(160.0)
        
        future_date = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
        result = visa_app.schedule_appointment(future_date, "14:30")
        
        assert "Appointment scheduled successfully" in result
        assert future_date in result
        assert "at 14:30" in result
        assert visa_app.appointment["time"] == "14:30"
    
    def test_schedule_appointment_past_date(self, visa_app):
        """Test scheduling appointment with past date should raise ValueError"""
        from datetime import datetime, timedelta
        
        visa_app.select_visa_type("B1/B2")
        visa_app.pay_fee(160.0)
        
        past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        with pytest.raises(ValueError) as exc_info:
            visa_app.schedule_appointment(past_date)
        assert "Appointment date must be in the future" in str(exc_info.value)
    
    def test_schedule_appointment_today(self, visa_app):
        """Test scheduling appointment for today should raise ValueError"""
        from datetime import datetime
        
        visa_app.select_visa_type("B1/B2")
        visa_app.pay_fee(160.0)
        
        today = datetime.now().strftime("%Y-%m-%d")
        with pytest.raises(ValueError) as exc_info:
            visa_app.schedule_appointment(today)
        assert "Appointment date must be in the future" in str(exc_info.value)
    
    def test_schedule_appointment_no_payment(self, visa_app):
        """Test scheduling appointment without payment should raise ValueError"""
        from datetime import datetime, timedelta
        
        visa_app.select_visa_type("B1/B2")
        
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        with pytest.raises(ValueError) as exc_info:
            visa_app.schedule_appointment(future_date)
        assert "Payment must be completed before scheduling an appointment" in str(exc_info.value)
    
    def test_schedule_appointment_invalid_date_format(self, visa_app):
        """Test scheduling appointment with invalid date format should raise ValueError"""
        visa_app.select_visa_type("B1/B2")
        visa_app.pay_fee(160.0)
        
        with pytest.raises(ValueError) as exc_info:
            visa_app.schedule_appointment("2025-13-45")
        assert "Invalid date format" in str(exc_info.value)
        assert "YYYY-MM-DD format" in str(exc_info.value)
    
    def test_schedule_appointment_empty_input(self, visa_app):
        """Test scheduling appointment with empty date should raise ValueError"""
        visa_app.select_visa_type("B1/B2")
        visa_app.pay_fee(160.0)
        
        with pytest.raises(ValueError) as exc_info:
            visa_app.schedule_appointment("")
        assert "Appointment date must be provided as a non-empty string" in str(exc_info.value)
    
    def test_collect_biometrics(self, visa_app):
        """Test biometric collection functionality"""
        pass
    
    def test_interview(self, visa_app):
        """Test visa interview functionality"""
        pass
    
    def test_process_application(self, visa_app):
        """Test application processing functionality"""
        pass
    
    def test_issue_visa(self, visa_app):
        """Test visa issuance functionality"""
        pass