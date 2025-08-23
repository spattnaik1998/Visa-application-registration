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
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()