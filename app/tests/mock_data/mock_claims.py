from datetime import datetime

MOCK_CLAIMS = [
    {
        "ClaimId": "b4f1d268-d04b-4e17-b93e-2dc9d21d739e",
        "ClaimName": "Xray Hand",
        "ClaimAmount": 80.6,
        "ClaimStatus": "Initiated",
        "ClaimDate": datetime(2026, 8, 18, 5, 56),
        "ClaimCloseEstimation": datetime(2026, 11, 26, 5, 56),
        "ClaimTPA": "CNC",
        "ClaimTin": "12345",
        "ClaimAuditTime": datetime(2026, 11, 16, 5, 56),
        "ClaimPlaceOfService": "Chirala",
        "ClaimProviderId": "0b12dd95-5cf5-4e4c-943e-ea98bbbc0fcf",
    },
    {
        "ClaimId": "c5f1d268-d04b-4e17-b93e-2dc9d21d739e",
        "ClaimName": "Blood Test",
        "ClaimAmount": 150.0,
        "ClaimStatus": "Initiated",
        "ClaimDate": datetime(2026, 8, 20, 9, 30),
        "ClaimCloseEstimation": datetime(2026, 11, 28, 9, 30),
        "ClaimTPA": "ABC",
        "ClaimTin": "67890",
        "ClaimAuditTime": datetime(2026, 11, 16, 10, 30),
        "ClaimPlaceOfService": "Ongole",
        "ClaimProviderId": "1b12dd95-5cf5-4e4c-943e-ea98bbbc0fcf",
    },
]

MOCK_PROVIDERS = [
    {
        "ProviderId": "0b12dd95-5cf5-4e4c-943e-ea98bbbc0fcf",
        "ProviderName": "Vijaya Labs",
        "ProviderMail": "vijayalabs@gmail.com",
        "ProviderType": "Hospital",
        "TIN": "12345678",
        "ProviderPassword": "password123",
    }
]

MOCK_PLACES = [
    {
        "PlaceOfServiceCd": "Chirala",
        "PlacePinCode": "523155",
        "PlaceDistrict": "Bapatla",
        "PlaceState": "Andhra Pradesh",
    }
]
