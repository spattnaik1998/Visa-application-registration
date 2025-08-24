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