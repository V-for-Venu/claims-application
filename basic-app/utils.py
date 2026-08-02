from claims_data import claims_data
from requests import Session
from constants import add_claims_url, claim_names, claim_status
from random import choice, random, randint
from datetime import date, timedelta
import time

def claim_exists(claim_id: int) -> bool:
    """
    Check if Claim ID Exists in claims_data.
    """
    return claim_id in claims_data.keys()


def generate_data(n=5):
    """
    Generate Random Claim Data 
    """
    with Session() as session:
        for _ in range(n):
            random_data = {
                "ClaimName": choice(claim_names),
                "ClaimAmount": round(random() * 100, 2),
                "ClaimStatus": choice(claim_status),
                "ClaimDate": (date.today() - timedelta(days=randint(1, 90))).isoformat()
            }
            time.sleep(0.5)
            try:
                response = session.post(add_claims_url, json=random_data)
                if response.status_code == 200:
                    print(response.json()['message'])
                else:
                    print(f"Error Adding Claims: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Error occurred while adding Claims: {str(e)}")
                

if __name__ == "__main__":
    generate_data(int(input("Enter Random Claim Data Count to Generate: ")))
