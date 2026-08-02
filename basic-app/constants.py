from datetime import date, timedelta
from random import randint

# Basic APP Local Host URLs
add_claims_url = "http://localhost:8000/add/claims"

# Claim Data Generation Constants
claim_names = [
    "Annual Physical Examination",
    "Full Body Health Checkup",
    "Routine Dental Checkup & Cleaning",
    "Dental Cavity Filling",
    "Comprehensive Eye Examination",
    "Prescription Eyeglasses Invoicing",
    "Complete Blood Count (CBC) Lab Test",
    "Chest X-Ray Digital Imaging",
    "Chronic Medication Prescription Refill",
    "Emergency Room Acute Care"
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