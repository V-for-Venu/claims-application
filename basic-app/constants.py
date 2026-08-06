from datetime import date, timedelta
from random import randint

# Basic APP Local Host URLs
add_claims_url = "http://localhost:8000/add/claims"

# Claim Data Generation Constants
claim_names = [
    "Full Body Checkup",
    "Routine Blood Test",
    "Dental Checkup",
    "Tooth Extraction",
    "Chest X-Ray",
    "Brain MRI Scan",
    "Eye Examination",
    "Doctor Consultation",
    "Prescription Medicine",
    "Physical Therapy",
    "Heart ECG Test",
    "Ultrasound Scan",
    "Cavity Filling",
    "Flu Vaccination",
    "Skin Clinic Visit",
    "Emergency Room Care",
    "Allergy Testing",
    "Spine CT Scan",
    "Diabetes Screening",
    "Surgical Consultation"
]


claim_status = [
    "Pending",
    "Approved",
    "Rejected"
]

def random_date_last_90_days():
    """
    Generates Random date within Last 90 Days from Today
    """
    return (date.today() - timedelta(days=randint(1, 90)))