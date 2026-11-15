import requests
import os
import hmac
import hashlib

from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ----------------------------------
# 1. Load environment variables
# ----------------------------------

load_dotenv()

API_KEY = os.getenv("API_KEY")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

if not API_KEY or not WEBHOOK_SECRET:
    raise ValueError("Missing API_KEY or WEBHOOK_SECRET in .env file")


# ----------------------------------
# 2. Create requests session
#    with retry configuration
# ----------------------------------

def create_session():

    session = requests.Session()

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    session.headers.update({
        "Authorization": f"Bearer {API_KEY}"
    })

    return session


# STEP 3: Get first 5 users from API
def get_users():

    session = create_session()

    url = "https://jsonplaceholder.typicode.com/users"

    response = session.get(url, timeout=10)

    response.raise_for_status()

    users = response.json()

    for user in users[:5]:

        print(
            f"{user.get('id')} - "
            f"{user.get('name')} - "
            f"{user.get('email')}"
        )

    # STEP 4: Get nested JSON details
    first_user = users[0]

    address = first_user.get("address", {})
    geo = address.get("geo", {})
    company = first_user.get("company", {})

    city = address.get("city", "Not Available")
    latitude = geo.get("lat", "Not Available")
    zip_code = address.get("zipcode", "Not Available")
    company_name = company.get("name", "Not Available")

    print("\nFirst User Details")

    print("City:", city)
    print("Latitude:", latitude)
    print("Zip:", zip_code)
    print("Company:", company_name)


# STEP 5: Verify webhook signature
def verify_signature(payload, signature, secret):

    expected_signature = hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        expected_signature,
        signature
    )


# STEP 6: Test webhook security
def test_webhook():

    payload = b'{"employee": "Shruti", "salary": 50000}'

    valid_signature = hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()

    tampered_payload = b'{"employee": "Shruti", "salary": 60000}'

    wrong_secret_signature = hmac.new(
        b"wrong_secret",
        payload,
        hashlib.sha256
    ).hexdigest()

    valid = verify_signature(
        payload,
        valid_signature,
        WEBHOOK_SECRET
    )

    tampered = verify_signature(
        tampered_payload,
        valid_signature,
        WEBHOOK_SECRET
    )

    wrong_secret = verify_signature(
        payload,
        wrong_secret_signature,
        WEBHOOK_SECRET
    )

    print("\nWebhook Security Results")

    print("Valid:", valid)
    print("Tampered:", tampered)
    print("Wrong secret:", wrong_secret)


# MAIN PROGRAM
if __name__ == "__main__":

    print("API CLIENT RESULTS\n")

    get_users()

    test_webhook()