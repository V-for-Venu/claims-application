from uuid import UUID

from database.claim_sql_model import Claims, PlaceOfService, Provider

from .mock_claims import MOCK_CLAIMS, MOCK_PLACES, MOCK_PROVIDERS


async def insert_mock_data(session):

    # Convert Provider IDs from str to UUID
    providers = [
        Provider(
            **{
                **provider_data,
                "ProviderId": UUID(provider_data["ProviderId"]),
            }
        )
        for provider_data in MOCK_PROVIDERS
    ]

    # Create Place of Service objects
    places = [PlaceOfService(**place_data) for place_data in MOCK_PLACES]

    session.add_all(providers)
    session.add_all(places)

    await session.flush()

    # Convert Claim IDs and Provider IDs from str to UUID
    claims = [
        Claims(
            **{
                **claim_data,
                "ClaimId": UUID(claim_data["ClaimId"]),
                "ClaimProviderId": UUID(claim_data["ClaimProviderId"]),
            }
        )
        for claim_data in MOCK_CLAIMS
    ]

    session.add_all(claims)

    await session.commit()
