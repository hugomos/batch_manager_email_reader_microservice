import os
import requests


def authenticate(email, password):
    auth_url = os.getenv("AUTH_API_URL")
    response = requests.post(auth_url, json={"email": email, "password": password})
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return True
    return False
