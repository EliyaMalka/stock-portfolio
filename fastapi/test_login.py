import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_login():
    # 1. Create a user (if not exists)
    username = "testloginuser"
    password = "securepassword123"
    email = "testlogin@example.com"

    print(f"Creating user {username}...")
    try:
        r = requests.post(f"{BASE_URL}/users", json={
            "Username": username,
            "Email": email,
            "Password": password
        })
        if r.status_code == 201:
            print("User created.")
        elif r.status_code == 400: # Probably already exists
            print("User already exists (expected).")
        else:
            print(f"Failed to create user: {r.status_code} {r.text}")
            return
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is it running on port 8000?")
        return

    # 2. Test Login
    print(f"Testing login for {username}...")
    login_payload = {
        "Username": username,
        "Password": password
    }
    
    r = requests.post(f"{BASE_URL}/login", json=login_payload)
    
    if r.status_code == 200:
        print("Login SUCCESS!")
        print("Response:", r.json())
    else:
        print(f"Login FAILED: {r.status_code} {r.text}")

if __name__ == "__main__":
    test_login()
