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