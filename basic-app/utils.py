import time
from datetime import datetime, timedelta, timezone
from random import choice, randint, random
from uuid import uuid4

from claims_data import claims_data
from constants import (
    add_claims_url,
    claim_names,
    claim_status,
    claim_TPA,
    place_of_service,
)
from requests import Session


def claim_exists(claim_id: int) -> bool:
    """
    Check if Claim ID Exists in claims_data.
    """
    return claim_id in claims_data


def generate_data(n=5):
    """
    Generate Random Claim Data
    """
    with Session() as session:
        for _ in range(n):
            random_data = {
                "ClaimName": choice(claim_names),
                "ClaimAmount": round(random() * 1000, 2),
                "ClaimStatus": choice(claim_status),
                "ClaimDate": (
                    datetime.now(tz=timezone.utc) - timedelta(days=randint(1, 90))
                ).isoformat(),
                "ClaimCloseEstimation": (
                    datetime.now(tz=timezone.utc) + timedelta(days=randint(1, 90))
                ).isoformat(),
                "ClaimTPA": choice(claim_TPA),
                "ClaimUniqueId": str(uuid4()),
                "ClaimTin": f"{randint(100000000, 999999999)}",
                "ClaimPlaceOfService": choice(place_of_service),
            }
            time.sleep(0.5)
            try:
                response = session.post(add_claims_url, json=random_data)
                if response.status_code == 200:
                    print(response.json()["detail"])
                else:
                    print(
                        f"Error Adding Claims: {response.status_code} - {response.text}"
                    )
            except Exception as e:  # noqa: BLE001
                print(f"Error occurred while adding Claims: {e}")


if __name__ == "__main__":
    generate_data(int(input("Enter Random Claim Data Count to Generate: ")))
