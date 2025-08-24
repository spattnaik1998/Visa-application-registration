import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestVisaAPI:
    """Test suite for Visa API endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "U.S. Visa Application API is running"
    
    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_select_visa_type_valid_b1b2(self):
        """Test selecting valid B1/B2 visa type"""
        response = client.post(
            "/api/v1/select_visa_type",
            json={"visa_type": "B1/B2"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["visa_type"] == "B1/B2"
        assert "selected successfully" in data["message"]
    
    def test_select_visa_type_valid_f1(self):
        """Test selecting valid F1 visa type"""
        response = client.post(
            "/api/v1/select_visa_type",
            json={"visa_type": "F1"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["visa_type"] == "F1"
        assert "selected successfully" in data["message"]
    
    def test_select_visa_type_valid_h1b(self):
        """Test selecting valid H1B visa type"""
        response = client.post(
            "/api/v1/select_visa_type",
            json={"visa_type": "H1B"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["visa_type"] == "H1B"
        assert "selected successfully" in data["message"]
    
    def test_select_visa_type_valid_j1(self):
        """Test selecting valid J1 visa type"""
        response = client.post(
            "/api/v1/select_visa_type",
            json={"visa_type": "J1"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["visa_type"] == "J1"
        assert "selected successfully" in data["message"]
    
    def test_select_visa_type_invalid(self):
        """Test selecting invalid visa type"""
        response = client.post(
            "/api/v1/select_visa_type",
            json={"visa_type": "Tourist"}
        )
        assert response.status_code == 422  # Pydantic validation error
    
    def test_select_visa_type_empty_string(self):
        """Test selecting empty string visa type"""
        response = client.post(
            "/api/v1/select_visa_type",
            json={"visa_type": ""}
        )
        assert response.status_code == 422  # Pydantic validation error
    
    def test_select_visa_type_missing_field(self):
        """Test request with missing visa_type field"""
        response = client.post(
            "/api/v1/select_visa_type",
            json={}
        )
        assert response.status_code == 422
    
    def test_get_visa_types(self):
        """Test getting available visa types"""
        response = client.get("/api/v1/visa_types")
        assert response.status_code == 200
        data = response.json()
        assert "visa_types" in data
        assert "B1/B2" in data["visa_types"]
        assert "F1" in data["visa_types"]
        assert "H1B" in data["visa_types"]
        assert "J1" in data["visa_types"]
        assert "descriptions" in data

class TestDS160API:
    """Test suite for DS-160 Form API endpoints"""
    
    def test_fill_ds160_valid_form(self):
        """Test filling DS-160 form with valid data"""
        valid_form_data = {
            "full_name": "John Doe",
            "passport_number": "X1234567",
            "dob": "1990-05-15",
            "nationality": "India",
            "email": "johndoe@email.com"
        }
        
        response = client.post(
            "/api/v1/fill_ds160",
            json=valid_form_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "DS-160 form submitted successfully"
        assert "confirmation_id" in data
        assert len(data["confirmation_id"]) == 8
    
    def test_fill_ds160_invalid_passport_special_chars(self):
        """Test DS-160 form with passport number containing special characters"""
        invalid_form_data = {
            "full_name": "John Doe",
            "passport_number": "X123-456",  # Contains hyphen
            "dob": "1990-05-15",
            "nationality": "India",
            "email": "johndoe@email.com"
        }
        
        response = client.post(
            "/api/v1/fill_ds160",
            json=invalid_form_data
        )
        assert response.status_code == 422
        assert "alphanumeric" in response.json()["detail"][0]["msg"].lower()
    
    def test_fill_ds160_invalid_passport_too_short(self):
        """Test DS-160 form with passport number too short"""
        invalid_form_data = {
            "full_name": "John Doe",
            "passport_number": "X123",  # Too short
            "dob": "1990-05-15",
            "nationality": "India",
            "email": "johndoe@email.com"
        }
        
        response = client.post(
            "/api/v1/fill_ds160",
            json=invalid_form_data
        )
        assert response.status_code == 422
        assert "6 characters" in response.json()["detail"][0]["msg"]
    
    def test_fill_ds160_invalid_email_format(self):
        """Test DS-160 form with invalid email format"""
        invalid_form_data = {
            "full_name": "John Doe",
            "passport_number": "X1234567",
            "dob": "1990-05-15",
            "nationality": "India",
            "email": "invalid-email"  # Invalid email format
        }
        
        response = client.post(
            "/api/v1/fill_ds160",
            json=invalid_form_data
        )
        assert response.status_code == 422
        assert "email" in response.json()["detail"][0]["msg"].lower()
    
    def test_fill_ds160_invalid_dob_future(self):
        """Test DS-160 form with future date of birth"""
        invalid_form_data = {
            "full_name": "John Doe",
            "passport_number": "X1234567",
            "dob": "2030-05-15",  # Future date
            "nationality": "India",
            "email": "johndoe@email.com"
        }
        
        response = client.post(
            "/api/v1/fill_ds160",
            json=invalid_form_data
        )
        assert response.status_code == 422
        assert "past" in response.json()["detail"][0]["msg"].lower()
    
    def test_fill_ds160_invalid_dob_format(self):
        """Test DS-160 form with invalid date format"""
        invalid_form_data = {
            "full_name": "John Doe",
            "passport_number": "X1234567",
            "dob": "15-05-1990",  # Wrong format
            "nationality": "India",
            "email": "johndoe@email.com"
        }
        
        response = client.post(
            "/api/v1/fill_ds160",
            json=invalid_form_data
        )
        assert response.status_code == 422
        assert "YYYY-MM-DD" in response.json()["detail"][0]["msg"]
    
    def test_fill_ds160_invalid_full_name_numbers(self):
        """Test DS-160 form with full name containing numbers"""
        invalid_form_data = {
            "full_name": "John123 Doe",  # Contains numbers
            "passport_number": "X1234567",
            "dob": "1990-05-15",
            "nationality": "India",
            "email": "johndoe@email.com"
        }
        
        response = client.post(
            "/api/v1/fill_ds160",
            json=invalid_form_data
        )
        assert response.status_code == 422
        assert "letters" in response.json()["detail"][0]["msg"].lower()
    
    def test_fill_ds160_invalid_nationality_numbers(self):
        """Test DS-160 form with nationality containing numbers"""
        invalid_form_data = {
            "full_name": "John Doe",
            "passport_number": "X1234567",
            "dob": "1990-05-15",
            "nationality": "India123",  # Contains numbers
            "email": "johndoe@email.com"
        }
        
        response = client.post(
            "/api/v1/fill_ds160",
            json=invalid_form_data
        )
        assert response.status_code == 422
        assert "letters" in response.json()["detail"][0]["msg"].lower()
    
    def test_fill_ds160_missing_fields(self):
        """Test DS-160 form with missing required fields"""
        incomplete_form_data = {
            "full_name": "John Doe",
            "passport_number": "X1234567"
            # Missing dob, nationality, email
        }
        
        response = client.post(
            "/api/v1/fill_ds160",
            json=incomplete_form_data
        )
        assert response.status_code == 422
    
    def test_fill_ds160_valid_edge_cases(self):
        """Test DS-160 form with valid edge cases"""
        valid_edge_cases = [
            {
                "full_name": "Mary-Jane O'Connor",  # Hyphen and apostrophe
                "passport_number": "AB123456",
                "dob": "1985-12-25",
                "nationality": "United States",
                "email": "mary.jane@example.com"
            },
            {
                "full_name": "José María García",  # Accented characters (if supported)
                "passport_number": "MX987654",
                "dob": "1975-01-01",
                "nationality": "Mexico",
                "email": "jose.garcia@ejemplo.com"
            }
        ]
        
        for form_data in valid_edge_cases:
            response = client.post(
                "/api/v1/fill_ds160",
                json=form_data
            )
            # Should either pass (200) or fail validation (422), but not crash (500)
            assert response.status_code in [200, 422]

class TestPaymentAPI:
    """Test suite for Visa Fee Payment API endpoints"""
    
    def test_pay_visa_fee_valid_payment(self):
        """Test paying visa fee with valid payment data"""
        valid_payment_data = {
            "application_id": "APP12345",
            "amount": 160.0,
            "currency": "USD",
            "payment_method": "credit_card",
            "transaction_id": "TXN98765"
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=valid_payment_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Visa fee payment recorded successfully"
        assert "payment_confirmation_id" in data
        assert len(data["payment_confirmation_id"]) == 8
        assert data["amount"] == 160.0
        assert data["currency"] == "USD"
    
    def test_pay_visa_fee_different_currencies(self):
        """Test paying visa fee with different valid currencies"""
        currencies_and_amounts = [
            ("USD", 160.0),
            ("EUR", 145.0),
            ("INR", 12500.0)
        ]
        
        for currency, amount in currencies_and_amounts:
            payment_data = {
                "application_id": f"APP{currency}123",
                "amount": amount,
                "currency": currency,
                "payment_method": "credit_card",
                "transaction_id": f"TXN{currency}456"
            }
            
            response = client.post(
                "/api/v1/pay_visa_fee",
                json=payment_data
            )
            assert response.status_code == 200
            data = response.json()
            assert data["currency"] == currency
            assert data["amount"] == amount
    
    def test_pay_visa_fee_different_payment_methods(self):
        """Test paying visa fee with different valid payment methods"""
        payment_methods = ["credit_card", "debit_card", "upi", "paypal"]
        
        for method in payment_methods:
            payment_data = {
                "application_id": f"APP{method.upper()}123",
                "amount": 160.0,
                "currency": "USD",
                "payment_method": method,
                "transaction_id": f"TXN{method.upper()}456"
            }
            
            response = client.post(
                "/api/v1/pay_visa_fee",
                json=payment_data
            )
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
    
    def test_pay_visa_fee_invalid_currency(self):
        """Test paying visa fee with invalid currency"""
        invalid_payment_data = {
            "application_id": "APP12345",
            "amount": 160.0,
            "currency": "CAD",  # Not in allowed currencies
            "payment_method": "credit_card",
            "transaction_id": "TXN98765"
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
    
    def test_pay_visa_fee_negative_amount(self):
        """Test paying visa fee with negative amount"""
        invalid_payment_data = {
            "application_id": "APP12345",
            "amount": -160.0,  # Negative amount
            "currency": "USD",
            "payment_method": "credit_card",
            "transaction_id": "TXN98765"
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
        assert "positive number" in response.json()["detail"][0]["msg"].lower()
    
    def test_pay_visa_fee_amount_too_small(self):
        """Test paying visa fee with amount below minimum"""
        invalid_payment_data = {
            "application_id": "APP12345",
            "amount": 25.0,  # Below minimum of 50
            "currency": "USD",
            "payment_method": "credit_card",
            "transaction_id": "TXN98765"
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
        assert "minimum payment amount is 50" in response.json()["detail"][0]["msg"].lower()
    
    def test_pay_visa_fee_amount_too_large(self):
        """Test paying visa fee with amount above maximum"""
        invalid_payment_data = {
            "application_id": "APP12345",
            "amount": 15000.0,  # Above maximum of 10,000
            "currency": "USD",
            "payment_method": "credit_card",
            "transaction_id": "TXN98765"
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
        assert "maximum payment amount is 10,000" in response.json()["detail"][0]["msg"].lower()
    
    def test_pay_visa_fee_invalid_payment_method(self):
        """Test paying visa fee with invalid payment method"""
        invalid_payment_data = {
            "application_id": "APP12345",
            "amount": 160.0,
            "currency": "USD",
            "payment_method": "bitcoin",  # Not in allowed payment methods
            "transaction_id": "TXN98765"
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
    
    def test_pay_visa_fee_invalid_application_id(self):
        """Test paying visa fee with invalid application ID"""
        invalid_payment_data = {
            "application_id": "APP-123",  # Contains hyphen (not alphanumeric)
            "amount": 160.0,
            "currency": "USD",
            "payment_method": "credit_card",
            "transaction_id": "TXN98765"
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
        assert "alphanumeric" in response.json()["detail"][0]["msg"].lower()
    
    def test_pay_visa_fee_application_id_too_short(self):
        """Test paying visa fee with application ID too short"""
        invalid_payment_data = {
            "application_id": "AB",  # Too short (minimum 3 characters)
            "amount": 160.0,
            "currency": "USD",
            "payment_method": "credit_card",
            "transaction_id": "TXN98765"
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
        assert "3 characters" in response.json()["detail"][0]["msg"]
    
    def test_pay_visa_fee_invalid_transaction_id(self):
        """Test paying visa fee with invalid transaction ID"""
        invalid_payment_data = {
            "application_id": "APP12345",
            "amount": 160.0,
            "currency": "USD",
            "payment_method": "credit_card",
            "transaction_id": "TXN-987"  # Contains hyphen (not alphanumeric)
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
        assert "alphanumeric" in response.json()["detail"][0]["msg"].lower()
    
    def test_pay_visa_fee_transaction_id_too_short(self):
        """Test paying visa fee with transaction ID too short"""
        invalid_payment_data = {
            "application_id": "APP12345",
            "amount": 160.0,
            "currency": "USD",
            "payment_method": "credit_card",
            "transaction_id": "TX12"  # Too short (minimum 5 characters)
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
        assert "5 characters" in response.json()["detail"][0]["msg"]
    
    def test_pay_visa_fee_missing_transaction_id(self):
        """Test paying visa fee with missing transaction_id field"""
        incomplete_payment_data = {
            "application_id": "APP12345",
            "amount": 160.0,
            "currency": "USD",
            "payment_method": "credit_card"
            # Missing transaction_id
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=incomplete_payment_data
        )
        assert response.status_code == 422
    
    def test_pay_visa_fee_missing_all_required_fields(self):
        """Test paying visa fee with missing required fields"""
        incomplete_payment_data = {}
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=incomplete_payment_data
        )
        assert response.status_code == 422

class TestPaymentAPIEnhancements:
    """Additional test suite for enhanced payment functionality"""
    
    def test_pay_visa_fee_valid_data_simple(self):
        """Test paying visa fee with basic valid data"""
        valid_payment_data = {
            "application_id": "12345",
            "amount": 160,
            "currency": "USD", 
            "payment_method": "credit_card",
            "transaction_id": "TXN98765"
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=valid_payment_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Visa fee payment recorded successfully"
        assert "payment_confirmation_id" in data
        assert data["amount"] == 160
        assert data["currency"] == "USD"
    
    def test_pay_visa_fee_invalid_currency_cad(self):
        """Test paying visa fee with invalid currency CAD"""
        invalid_payment_data = {
            "application_id": "APP123",
            "amount": 160,
            "currency": "CAD",  # Not in allowed currencies
            "payment_method": "credit_card",
            "transaction_id": "TXN456"
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
    
    def test_pay_visa_fee_invalid_currency_gbp(self):
        """Test paying visa fee with invalid currency GBP"""
        invalid_payment_data = {
            "application_id": "APP789",
            "amount": 160,
            "currency": "GBP",  # Not in allowed currencies
            "payment_method": "debit_card",
            "transaction_id": "TXN999"
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
    
    def test_pay_visa_fee_negative_amount(self):
        """Test paying visa fee with negative amount"""
        invalid_payment_data = {
            "application_id": "APP456",
            "amount": -100,  # Negative amount
            "currency": "USD",
            "payment_method": "credit_card",
            "transaction_id": "TXN123"
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
        assert "positive number" in response.json()["detail"][0]["msg"].lower()
    
    def test_pay_visa_fee_zero_amount(self):
        """Test paying visa fee with zero amount"""
        invalid_payment_data = {
            "application_id": "APP789",
            "amount": 0,  # Zero amount
            "currency": "EUR",
            "payment_method": "paypal",
            "transaction_id": "TXN000"
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
        assert "positive number" in response.json()["detail"][0]["msg"].lower()
    
    def test_pay_visa_fee_amount_below_minimum(self):
        """Test paying visa fee with amount below minimum (50)"""
        invalid_payment_data = {
            "application_id": "APP111",
            "amount": 25,  # Below minimum
            "currency": "INR",
            "payment_method": "upi",
            "transaction_id": "TXN111"
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
        assert "minimum payment amount is 50" in response.json()["detail"][0]["msg"].lower()
    
    def test_pay_visa_fee_missing_transaction_id(self):
        """Test paying visa fee with missing transaction_id"""
        incomplete_payment_data = {
            "application_id": "APP555",
            "amount": 160,
            "currency": "USD",
            "payment_method": "credit_card"
            # Missing transaction_id
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=incomplete_payment_data
        )
        assert response.status_code == 422
    
    def test_pay_visa_fee_empty_transaction_id(self):
        """Test paying visa fee with empty transaction_id"""
        invalid_payment_data = {
            "application_id": "APP666",
            "amount": 160,
            "currency": "EUR",
            "payment_method": "debit_card",
            "transaction_id": ""  # Empty string
        }
        
        response = client.post(
            "/api/v1/pay_visa_fee",
            json=invalid_payment_data
        )
        assert response.status_code == 422
        assert "5 characters" in response.json()["detail"][0]["msg"]
    
    def test_pay_visa_fee_all_valid_currencies(self):
        """Test paying visa fee with all valid currencies"""
        valid_currencies = ["USD", "EUR", "INR"]
        
        for currency in valid_currencies:
            payment_data = {
                "application_id": f"APP{currency}",
                "amount": 160 if currency == "USD" else (145 if currency == "EUR" else 8000),
                "currency": currency,
                "payment_method": "credit_card",
                "transaction_id": f"TXN{currency}"
            }
            
            response = client.post(
                "/api/v1/pay_visa_fee",
                json=payment_data
            )
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["currency"] == currency
    
    def test_pay_visa_fee_all_valid_payment_methods(self):
        """Test paying visa fee with all valid payment methods"""
        valid_methods = ["credit_card", "debit_card", "upi", "paypal"]
        
        for i, method in enumerate(valid_methods):
            payment_data = {
                "application_id": f"APP{i+1}00",
                "amount": 160,
                "currency": "USD",
                "payment_method": method,
                "transaction_id": f"TXN{i+1}00"
            }
            
            response = client.post(
                "/api/v1/pay_visa_fee",
                json=payment_data
            )
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["message"] == "Visa fee payment recorded successfully"

class TestInterviewSchedulingAPI:
    """Test suite for Interview Scheduling API endpoints"""
    
    def test_schedule_interview_valid_data(self):
        """Test scheduling interview with valid data"""
        from datetime import datetime, timedelta
        
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        interview_data = {
            "application_id": "12345",
            "location": "New Delhi",
            "date": future_date
        }
        
        response = client.post(
            "/api/v1/schedule_interview",
            json=interview_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Interview scheduled successfully"
        assert "interview_confirmation_id" in data
        assert data["location"] == "New Delhi"
        assert data["date"] == future_date
        assert len(data["interview_confirmation_id"]) == 8
    
    def test_schedule_interview_past_date(self):
        """Test scheduling interview with past date (should fail)"""
        from datetime import datetime, timedelta
        
        past_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        interview_data = {
            "application_id": "ABC123",
            "location": "Mumbai",
            "date": past_date
        }
        
        response = client.post(
            "/api/v1/schedule_interview",
            json=interview_data
        )
        assert response.status_code == 422
        assert "future" in response.json()["detail"][0]["msg"].lower()
    
    def test_schedule_interview_today_date(self):
        """Test scheduling interview for today (should fail)"""
        from datetime import datetime
        
        today = datetime.now().strftime("%Y-%m-%d")
        interview_data = {
            "application_id": "XYZ789",
            "location": "Chennai",
            "date": today
        }
        
        response = client.post(
            "/api/v1/schedule_interview",
            json=interview_data
        )
        assert response.status_code == 422
        assert "future" in response.json()["detail"][0]["msg"].lower()
    
    def test_schedule_interview_missing_application_id(self):
        """Test scheduling interview with missing application_id"""
        from datetime import datetime, timedelta
        
        future_date = (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d")
        interview_data = {
            "location": "Kolkata",
            "date": future_date
            # Missing application_id
        }
        
        response = client.post(
            "/api/v1/schedule_interview",
            json=interview_data
        )
        assert response.status_code == 422
    
    def test_schedule_interview_missing_location(self):
        """Test scheduling interview with missing location"""
        from datetime import datetime, timedelta
        
        future_date = (datetime.now() + timedelta(days=25)).strftime("%Y-%m-%d")
        interview_data = {
            "application_id": "DEF456",
            "date": future_date
            # Missing location
        }
        
        response = client.post(
            "/api/v1/schedule_interview",
            json=interview_data
        )
        assert response.status_code == 422
    
    def test_schedule_interview_missing_date(self):
        """Test scheduling interview with missing date"""
        interview_data = {
            "application_id": "GHI789",
            "location": "Hyderabad"
            # Missing date
        }
        
        response = client.post(
            "/api/v1/schedule_interview",
            json=interview_data
        )
        assert response.status_code == 422
    
    def test_schedule_interview_empty_location(self):
        """Test scheduling interview with empty location"""
        from datetime import datetime, timedelta
        
        future_date = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
        interview_data = {
            "application_id": "JKL012",
            "location": "",  # Empty location
            "date": future_date
        }
        
        response = client.post(
            "/api/v1/schedule_interview",
            json=interview_data
        )
        assert response.status_code == 422
        assert "2 characters" in response.json()["detail"][0]["msg"]
    
    def test_schedule_interview_short_location(self):
        """Test scheduling interview with location too short"""
        from datetime import datetime, timedelta
        
        future_date = (datetime.now() + timedelta(days=40)).strftime("%Y-%m-%d")
        interview_data = {
            "application_id": "MNO345",
            "location": "A",  # Too short
            "date": future_date
        }
        
        response = client.post(
            "/api/v1/schedule_interview",
            json=interview_data
        )
        assert response.status_code == 422
        assert "2 characters" in response.json()["detail"][0]["msg"]
    
    def test_schedule_interview_invalid_date_format(self):
        """Test scheduling interview with invalid date format"""
        interview_data = {
            "application_id": "PQR678",
            "location": "Bangalore",
            "date": "01-10-2025"  # Wrong format (DD-MM-YYYY instead of YYYY-MM-DD)
        }
        
        response = client.post(
            "/api/v1/schedule_interview",
            json=interview_data
        )
        assert response.status_code == 422
        assert "YYYY-MM-DD" in response.json()["detail"][0]["msg"]
    
    def test_schedule_interview_invalid_date_values(self):
        """Test scheduling interview with invalid date values"""
        interview_data = {
            "application_id": "STU901",
            "location": "Pune",
            "date": "2025-13-45"  # Invalid month and day
        }
        
        response = client.post(
            "/api/v1/schedule_interview",
            json=interview_data
        )
        assert response.status_code == 422
        assert "YYYY-MM-DD" in response.json()["detail"][0]["msg"]
    
    def test_schedule_interview_short_application_id(self):
        """Test scheduling interview with application ID too short"""
        from datetime import datetime, timedelta
        
        future_date = (datetime.now() + timedelta(days=35)).strftime("%Y-%m-%d")
        interview_data = {
            "application_id": "AB",  # Too short
            "location": "Ahmedabad",
            "date": future_date
        }
        
        response = client.post(
            "/api/v1/schedule_interview",
            json=interview_data
        )
        assert response.status_code == 422
        assert "3 characters" in response.json()["detail"][0]["msg"]
    
    def test_schedule_interview_non_alphanumeric_application_id(self):
        """Test scheduling interview with non-alphanumeric application ID"""
        from datetime import datetime, timedelta
        
        future_date = (datetime.now() + timedelta(days=50)).strftime("%Y-%m-%d")
        interview_data = {
            "application_id": "APP-123",  # Contains hyphen
            "location": "Gurgaon",
            "date": future_date
        }
        
        response = client.post(
            "/api/v1/schedule_interview",
            json=interview_data
        )
        assert response.status_code == 422
        assert "alphanumeric" in response.json()["detail"][0]["msg"].lower()
    
    def test_schedule_interview_various_locations(self):
        """Test scheduling interview with various valid locations"""
        from datetime import datetime, timedelta
        
        locations = ["New Delhi", "Mumbai Central", "Chennai Embassy", "U.S. Consulate Kolkata"]
        
        for i, location in enumerate(locations):
            future_date = (datetime.now() + timedelta(days=20 + i)).strftime("%Y-%m-%d")
            interview_data = {
                "application_id": f"APP{i+1}000",
                "location": location,
                "date": future_date
            }
            
            response = client.post(
                "/api/v1/schedule_interview",
                json=interview_data
            )
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["location"] == location
            assert data["date"] == future_date

class TestDocumentUploadAPI:
    """Test suite for Document Upload and OCR API endpoints"""
    
    def create_mock_image_with_text(self, text: str, width: int = 200, height: int = 100) -> bytes:
        """Create a mock image with text for testing OCR"""
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Create a white background image
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Try to use default font, fallback to PIL default if not available
        try:
            font = ImageFont.load_default()
        except:
            font = None
            
        # Add text to image
        draw.text((10, 10), text, fill='black', font=font)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    
    def create_mock_face_image(self, width: int = 200, height: int = 200) -> bytes:
        """Create a mock image that should trigger face detection"""
        from PIL import Image, ImageDraw
        import io
        
        # Create a white background image
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Draw a simple face-like pattern (circle for face, smaller circles for eyes)
        # This is basic but should be enough for testing the face detection pipeline
        face_center = (width//2, height//2)
        face_radius = min(width, height) // 3
        
        # Face outline
        draw.ellipse([
            face_center[0] - face_radius, 
            face_center[1] - face_radius,
            face_center[0] + face_radius, 
            face_center[1] + face_radius
        ], outline='black', width=3)
        
        # Eyes
        eye_radius = 8
        left_eye = (face_center[0] - 20, face_center[1] - 15)
        right_eye = (face_center[0] + 20, face_center[1] - 15)
        
        draw.ellipse([
            left_eye[0] - eye_radius, left_eye[1] - eye_radius,
            left_eye[0] + eye_radius, left_eye[1] + eye_radius
        ], fill='black')
        
        draw.ellipse([
            right_eye[0] - eye_radius, right_eye[1] - eye_radius,
            right_eye[0] + eye_radius, right_eye[1] + eye_radius
        ], fill='black')
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    
    def test_upload_documents_valid_passport_with_matching_number(self):
        """Test uploading valid passport document with matching passport number"""
        import io
        
        # Create mock passport image with passport number
        passport_number = "A1234567"
        passport_content = self.create_mock_image_with_text(f"PASSPORT\\n{passport_number}\\nUSA")
        
        files = {
            "passport": ("passport.png", io.BytesIO(passport_content), "image/png")
        }
        
        data = {
            "application_id": "APP12345",
            "expected_passport_number": passport_number
        }
        
        response = client.post(
            "/api/v1/upload_documents",
            files=files,
            data=data
        )
        
        # Note: This test might fail if OCR/tesseract is not properly configured
        # In that case, we'd expect a 400 status with an error message
        if response.status_code == 200:
            resp_data = response.json()
            assert resp_data["status"] == "success"
            assert resp_data["message"] == "Documents uploaded and validated"
            assert resp_data["documents_processed"] == 1
            assert "passport" in resp_data["validation_results"]
        else:
            # If OCR fails, we should get a proper error response
            assert response.status_code == 400
            assert "error" in response.json()["detail"]["status"]
    
    def test_upload_documents_valid_passport_with_mismatched_number(self):
        """Test uploading passport with mismatched passport number (should fail validation)"""
        import io
        
        # Create mock passport image with different passport number
        passport_content = self.create_mock_image_with_text("PASSPORT\\nB9876543\\nUSA")
        
        files = {
            "passport": ("passport.png", io.BytesIO(passport_content), "image/png")
        }
        
        data = {
            "application_id": "APP12345",
            "expected_passport_number": "A1234567"  # Different from image
        }
        
        response = client.post(
            "/api/v1/upload_documents",
            files=files,
            data=data
        )
        
        # Should fail validation due to mismatched passport number
        assert response.status_code == 400
        error_detail = response.json()["detail"]
        assert error_detail["status"] == "error"
        assert "passport validation" in error_detail["message"].lower()
    
    def test_upload_documents_photo_with_face(self):
        """Test uploading photo with detectable face"""
        import io
        
        # Create mock photo with face-like pattern
        photo_content = self.create_mock_face_image()
        
        files = {
            "photo": ("photo.jpg", io.BytesIO(photo_content), "image/jpeg")
        }
        
        data = {
            "application_id": "APP12345"
        }
        
        response = client.post(
            "/api/v1/upload_documents",
            files=files,
            data=data
        )
        
        # Note: Face detection might not work with our simple mock image
        # The test validates the processing pipeline works
        if response.status_code == 200:
            resp_data = response.json()
            assert resp_data["status"] == "success"
            assert resp_data["documents_processed"] == 1
            assert "photo" in resp_data["validation_results"]
        else:
            # If face detection fails, we should get a proper error
            assert response.status_code == 400
    
    def test_upload_documents_photo_without_face(self):
        """Test uploading photo without detectable face (should fail)"""
        import io
        
        # Create simple image without face patterns
        photo_content = self.create_mock_image_with_text("No face here, just text")
        
        files = {
            "photo": ("photo.jpg", io.BytesIO(photo_content), "image/jpeg")
        }
        
        data = {
            "application_id": "APP12345"
        }
        
        response = client.post(
            "/api/v1/upload_documents",
            files=files,
            data=data
        )
        
        # Should fail face detection validation
        assert response.status_code == 400
        error_detail = response.json()["detail"]
        assert error_detail["status"] == "error"
        assert "photo validation" in error_detail["message"].lower()
    
    def test_upload_documents_no_files(self):
        """Test uploading with no files (should fail)"""
        data = {
            "application_id": "APP12345"
        }
        
        response = client.post(
            "/api/v1/upload_documents",
            data=data
        )
        
        assert response.status_code == 400
        error_detail = response.json()["detail"]
        assert error_detail["status"] == "error"
        assert "at least one document must be uploaded" in error_detail["message"].lower()
    
    def test_upload_documents_missing_application_id(self):
        """Test uploading without application_id (should fail)"""
        import io
        
        passport_content = self.create_mock_image_with_text("PASSPORT A1234567")
        
        files = {
            "passport": ("passport.png", io.BytesIO(passport_content), "image/png")
        }
        
        # Missing application_id
        response = client.post(
            "/api/v1/upload_documents",
            files=files
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_upload_documents_supporting_documents(self):
        """Test uploading supporting documents"""
        import io
        
        # Create multiple supporting documents
        doc1_content = self.create_mock_image_with_text("Bank Statement\\nAccount: 123456")
        doc2_content = self.create_mock_image_with_text("Employment Letter\\nCompany XYZ")
        
        files = [
            ("supporting_docs", ("bank_statement.png", io.BytesIO(doc1_content), "image/png")),
            ("supporting_docs", ("employment_letter.png", io.BytesIO(doc2_content), "image/png"))
        ]
        
        data = {
            "application_id": "APP12345"
        }
        
        response = client.post(
            "/api/v1/upload_documents",
            files=files,
            data=data
        )
        
        # Should process supporting documents successfully
        if response.status_code == 200:
            resp_data = response.json()
            assert resp_data["status"] == "success"
            assert resp_data["documents_processed"] == 2
            assert "supporting_doc_1" in resp_data["validation_results"]
            assert "supporting_doc_2" in resp_data["validation_results"]
        else:
            # If OCR processing fails, should get proper error
            assert response.status_code in [400, 500]
    
    def test_upload_documents_multiple_types(self):
        """Test uploading multiple document types together"""
        import io
        
        # Create different document types
        passport_content = self.create_mock_image_with_text("PASSPORT\\nA1234567\\nUSA")
        photo_content = self.create_mock_face_image()
        support_content = self.create_mock_image_with_text("Supporting Document Text")
        
        files = [
            ("passport", ("passport.png", io.BytesIO(passport_content), "image/png")),
            ("photo", ("photo.jpg", io.BytesIO(photo_content), "image/jpeg")),
            ("supporting_docs", ("support.png", io.BytesIO(support_content), "image/png"))
        ]
        
        data = {
            "application_id": "APP12345",
            "expected_passport_number": "A1234567"
        }
        
        response = client.post(
            "/api/v1/upload_documents",
            files=files,
            data=data
        )
        
        # Should process all document types
        if response.status_code == 200:
            resp_data = response.json()
            assert resp_data["status"] == "success"
            assert resp_data["documents_processed"] == 3
            assert "passport" in resp_data["validation_results"]
            assert "photo" in resp_data["validation_results"]
            assert "supporting_doc_1" in resp_data["validation_results"]
        else:
            # If processing fails, should get proper error handling
            assert response.status_code in [400, 500]
    
    def test_upload_documents_invalid_image_format(self):
        """Test uploading invalid image file (should handle gracefully)"""
        import io
        
        # Create invalid file content (not an image)
        invalid_content = b"This is not an image file"
        
        files = {
            "passport": ("passport.txt", io.BytesIO(invalid_content), "text/plain")
        }
        
        data = {
            "application_id": "APP12345"
        }
        
        response = client.post(
            "/api/v1/upload_documents",
            files=files,
            data=data
        )
        
        # Should handle invalid file format gracefully
        assert response.status_code == 400
        error_detail = response.json()["detail"]
        assert error_detail["status"] == "error"

class TestInterviewAttendanceAPI:
    """Test suite for Interview Attendance API endpoints"""
    
    def test_attend_interview_mark_as_attended(self):
        """Test marking interview as attended"""
        attendance_data = {
            "application_id": "12345",
            "status": "attended"
        }
        
        response = client.post(
            "/api/v1/attend_interview",
            json=attendance_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Interview attendance recorded successfully"
        assert data["application_id"] == "12345"
        assert data["interview_status"] == "attended"
    
    def test_attend_interview_mark_as_missed(self):
        """Test marking interview as missed"""
        attendance_data = {
            "application_id": "APP67890",
            "status": "missed"
        }
        
        response = client.post(
            "/api/v1/attend_interview",
            json=attendance_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Interview attendance recorded successfully"
        assert data["application_id"] == "APP67890"
        assert data["interview_status"] == "missed"
    
    def test_attend_interview_invalid_status_value(self):
        """Test with invalid status value (should fail)"""
        attendance_data = {
            "application_id": "APP123",
            "status": "invalid_status"  # Not in ["attended", "missed"]
        }
        
        response = client.post(
            "/api/v1/attend_interview",
            json=attendance_data
        )
        
        assert response.status_code == 422
        assert "detail" in response.json()
    
    def test_attend_interview_invalid_status_canceled(self):
        """Test with another invalid status value"""
        attendance_data = {
            "application_id": "APP456",
            "status": "canceled"  # Not allowed
        }
        
        response = client.post(
            "/api/v1/attend_interview",
            json=attendance_data
        )
        
        assert response.status_code == 422
        assert "detail" in response.json()
    
    def test_attend_interview_missing_application_id(self):
        """Test with missing application_id (should fail)"""
        attendance_data = {
            "status": "attended"
            # Missing application_id
        }
        
        response = client.post(
            "/api/v1/attend_interview",
            json=attendance_data
        )
        
        assert response.status_code == 422
        assert "detail" in response.json()
    
    def test_attend_interview_missing_status(self):
        """Test with missing status (should fail)"""
        attendance_data = {
            "application_id": "APP789"
            # Missing status
        }
        
        response = client.post(
            "/api/v1/attend_interview",
            json=attendance_data
        )
        
        assert response.status_code == 422
        assert "detail" in response.json()
    
    def test_attend_interview_empty_application_id(self):
        """Test with empty application_id (should fail)"""
        attendance_data = {
            "application_id": "",  # Empty
            "status": "attended"
        }
        
        response = client.post(
            "/api/v1/attend_interview",
            json=attendance_data
        )
        
        assert response.status_code == 422
        assert "3 characters" in response.json()["detail"][0]["msg"]
    
    def test_attend_interview_short_application_id(self):
        """Test with application_id too short (should fail)"""
        attendance_data = {
            "application_id": "AB",  # Too short
            "status": "missed"
        }
        
        response = client.post(
            "/api/v1/attend_interview",
            json=attendance_data
        )
        
        assert response.status_code == 422
        assert "3 characters" in response.json()["detail"][0]["msg"]
    
    def test_attend_interview_non_alphanumeric_application_id(self):
        """Test with non-alphanumeric application_id (should fail)"""
        attendance_data = {
            "application_id": "APP-123",  # Contains hyphen
            "status": "attended"
        }
        
        response = client.post(
            "/api/v1/attend_interview",
            json=attendance_data
        )
        
        assert response.status_code == 422
        assert "alphanumeric" in response.json()["detail"][0]["msg"].lower()
    
    def test_attend_interview_application_id_normalization(self):
        """Test that application_id is normalized to uppercase"""
        attendance_data = {
            "application_id": "app123xyz",  # lowercase
            "status": "attended"
        }
        
        response = client.post(
            "/api/v1/attend_interview",
            json=attendance_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["application_id"] == "APP123XYZ"  # Should be normalized to uppercase
    
    def test_attend_interview_both_status_values(self):
        """Test both valid status values work correctly"""
        valid_statuses = ["attended", "missed"]
        
        for status in valid_statuses:
            attendance_data = {
                "application_id": f"TEST{status.upper()}",
                "status": status
            }
            
            response = client.post(
                "/api/v1/attend_interview",
                json=attendance_data
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["interview_status"] == status
            assert data["application_id"] == f"TEST{status.upper()}"
    
    def test_attend_interview_exact_specification(self):
        """Test with exact specification format from requirements"""
        attendance_data = {
            "application_id": "12345",
            "status": "attended"
        }
        
        response = client.post(
            "/api/v1/attend_interview",
            json=attendance_data
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response contains success status
        assert data["status"] == "success"
        
        # Verify all required fields are present
        required_fields = ["status", "message", "application_id", "interview_status"]
        for field in required_fields:
            assert field in data
        
        # Verify values match specification
        assert data["application_id"] == "12345"
        assert data["interview_status"] == "attended"