from fastapi import FastAPI
from app.api.visa import router as visa_router

app = FastAPI(
    title="U.S. Visa Application API",
    description="A comprehensive API for processing U.S. visa applications",
    version="1.0.0"
)

# Include visa-related routes
app.include_router(visa_router, prefix="/api/v1", tags=["visa"])

@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {"message": "U.S. Visa Application API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "visa-application-api"}