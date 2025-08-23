from app.visa_application import VisaApplication


def main():
    """
    Entry point for the visa application simulation.
    This will eventually orchestrate the entire visa application workflow.
    """
    visa_app = VisaApplication()
    print("Visa Application Simulation")
    print("=" * 40)
    
    try:
        print("Step 1: Select Visa Type")
        result = visa_app.select_visa_type("B1/B2")
        print(result)
        print(f"Current visa type: {visa_app.visa_type}")
        print()
        
        print("Step 2: Check Eligibility")
        eligibility_result = visa_app.check_eligibility()
        print(eligibility_result)
        print()
        
        print("Step 3: Gather Required Documents")
        documents = {"passport": True}
        document_result = visa_app.gather_documents(documents)
        print(document_result)
        print(f"Documents provided: {visa_app.documents}")
        print()
        
        print("Step 4: Fill DS-160 Form")
        form_data = {
            "full_name": "John Doe",
            "dob": "1990-01-01",
            "passport_number": "A12345678",
            "nationality": "India",
            "travel_purpose": "Tourism"
        }
        ds160_result = visa_app.fill_ds160(form_data)
        print(ds160_result)
        print(f"Form submitted for: {visa_app.ds160_form_data['full_name']}")
        print()
        
        print("Step 5: Pay Visa Fee")
        payment_result = visa_app.pay_fee(160.0)
        print(payment_result)
        print(f"Required fee for {visa_app.visa_type}: $160.00")
        print()
        
        print("Step 6: Schedule Appointment")
        from datetime import datetime, timedelta
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        appointment_result = visa_app.schedule_appointment(future_date, "10:30")
        print(appointment_result)
        print(f"Appointment details: {visa_app.appointment}")
        print()
        
        print("Step 7: Collect Biometrics")
        biometrics_result = visa_app.collect_biometrics()
        print(biometrics_result)
        print("Biometrics: Fingerprints and photo captured successfully")
        print()
        
        print("Step 8: Attend Consular Interview")
        interview_result = visa_app.interview()
        print(interview_result)
        print(f"Interview outcome: {visa_app.interview_result}")
        print()
        
        print("Step 9: Application Processing")
        processing_result = visa_app.process_application()
        print(processing_result)
        print(f"Processing status: {visa_app.processing_status}")
        print()
        
        print("Step 10: Visa Issuance")
        try:
            issuance_result = visa_app.issue_visa()
            print(issuance_result)
            print(f"Visa Number: {visa_app.visa_number}")
            print()
            
            print("🎉 CONGRATULATIONS! Your U.S. visa has been successfully issued! 🎉")
            print()
        except ValueError as visa_error:
            print(f"Visa issuance not possible: {visa_error}")
            print()
        
        print("COMPLETE APPLICATION SUMMARY:")
        print("=" * 50)
        print(f"Visa Type: {visa_app.visa_type}")
        print(f"Applicant: {visa_app.ds160_form_data.get('full_name', 'N/A')}")
        print(f"Passport Number: {visa_app.ds160_form_data.get('passport_number', 'N/A')}")
        print(f"Nationality: {visa_app.ds160_form_data.get('nationality', 'N/A')}")
        print()
        print("CONFIRMATION NUMBERS:")
        print(f"  DS-160 ID: {visa_app.ds160_confirmation_id}")
        print(f"  Payment ID: {visa_app.payment_confirmation_id}")
        print(f"  Biometrics ID: {visa_app.biometrics_confirmation_id}")
        print()
        print("FINAL RESULTS:")
        print(f"  Interview Result: {visa_app.interview_result}")
        print(f"  Processing Status: {visa_app.processing_status}")
        print(f"  Visa Number: {visa_app.visa_number if visa_app.visa_number else 'Not Issued'}")
        print("=" * 50)
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()