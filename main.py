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
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()