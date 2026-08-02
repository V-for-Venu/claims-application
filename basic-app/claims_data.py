from constants import random_date_last_90_days

claims_data = {
    12345: {
        "ClaimName": "Full Body Checkup",
        "ClaimAmount": 1000.00,
        "ClaimStatus": "Pending",
        "ClaimDate": random_date_last_90_days()
    },
    19203 : {
        "ClaimName": "Dental Checkup",
        "ClaimAmount": 500.00,
        "ClaimStatus": "Approved",
        "ClaimDate": random_date_last_90_days()
    },
    39121: {
        "ClaimName": "Vision Test",
        "ClaimAmount": 300.00,
        "ClaimStatus": "Rejected",
        "ClaimDate": random_date_last_90_days()
    },
    9231: {
        "ClaimName": "Physical Therapy",
        "ClaimAmount": 800.00,
        "ClaimStatus": "Pending",
        "ClaimDate": random_date_last_90_days()
    },
    12312: {
        "ClaimName": "Chiropractic Adjustment",
        "ClaimAmount": 600.00,
        "ClaimStatus": "Approved",
        "ClaimDate": random_date_last_90_days()
    }
}

