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