import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "http://localhost:5235/api"

def test_create_user():
    logging.info("Testing Create User...")
    payload = {
        "Username": "TestUser_BalanceCheck",
        "Email": "test_balance@example.com",
        "Password": "securepassword123"
    }
    # Clean up if exists (implementation detail, assuming delete endpoint works or ignoring error)
    # Ideally should delete first, but let's try create 
    
    response = requests.post(f"{BASE_URL}/users", json=payload)
    if response.status_code == 201:
        user = response.json()
        logging.info(f"User created: {user}")
        if user['Balance'] == 0.0:
            logging.info("PASS: Balance initialized to 0.0")
        else:
            logging.error(f"FAIL: Balance not 0.0, got {user['Balance']}")
        return user['UserID']
    elif response.status_code == 400: # Already exists?
        logging.info("User might already exist, trying to fetch...")
        # Try to find user to get ID (not implemented in clean way here without listing all)
        # For test simplicity, let's assume we proceed or fail.
        logging.warning("User creation failed (likely exists). Skipping creation.")
        return None
    else:
        logging.error(f"FAIL: Create user failed {response.status_code} - {response.text}")
        return None

def test_initial_buy_fail(user_id):
    logging.info("Testing Initial Buy (Should Fail due to 0 Balance)...")
    payload = {
        "UserID": user_id,
        "StockSymbol": "AAPL",
        "Quantity": 10,
        "PricePerStock": 150.00
    }
    response = requests.post(f"{BASE_URL}/transactions", json=payload)
    if response.status_code == 400 and "Insufficient funds" in response.text:
         logging.info("PASS: Transaction failed as expected due to insufficient funds.")
    else:
         logging.error(f"FAIL: Transaction should have failed but got {response.status_code} - {response.text}")

def test_balance_update_manual(user_id):
    # This might require a manual DB update if we don't have a deposit endpoint.
    # For now, let's assume we can sell short (if allowed? No, removing check constraint allows negative quantity, which ADDS balance)
    pass

def test_sell_to_add_balance(user_id):
    logging.info("Testing Sell (Negative Quantity) to Add Balance...")
    # Sell 5 stocks at 100 each = 500 added to balance
    # NOTE: Logic allows selling even if we don't own stock (short selling/naive implementation)
    payload = {
        "UserID": user_id,
        "StockSymbol": "AAPL",
        "Quantity": -5,
        "PricePerStock": 100.00
    }
    response = requests.post(f"{BASE_URL}/transactions", json=payload)
    if response.status_code == 201:
        logging.info("PASS: Sell transaction successful.")
        
        # Verify Balance
        user_resp = requests.get(f"{BASE_URL}/users/{user_id}")
        user = user_resp.json()
        if user['Balance'] == 500.0:
            logging.info(f"PASS: User balance updated to 500.0")
            return True
        else:
             logging.error(f"FAIL: User balance mismatch. Expected 500.0, got {user['Balance']}")
             return False
    else:
        logging.error(f"FAIL: Sell transaction failed {response.status_code} - {response.text}")
        return False

def test_buy_with_balance(user_id):
    logging.info("Testing Buy with Sufficient Balance...")
    # Buy 2 stocks at 150 = 300 cost. Balance should be 500 - 300 = 200.
    payload = {
        "UserID": user_id,
        "StockSymbol": "AAPL",
        "Quantity": 2,
        "PricePerStock": 150.00
    }
    response = requests.post(f"{BASE_URL}/transactions", json=payload)
    if response.status_code == 201:
        logging.info("PASS: Buy transaction successful.")
        
        # Verify Balance
        user_resp = requests.get(f"{BASE_URL}/users/{user_id}")
        user = user_resp.json()
        if user['Balance'] == 200.0:
            logging.info(f"PASS: User balance updated to 200.0")
        else:
             logging.error(f"FAIL: User balance mismatch. Expected 200.0, got {user['Balance']}")
    else:
        logging.error(f"FAIL: Buy transaction failed {response.status_code} - {response.text}")

if __name__ == "__main__":
    logging.info("Starting Verification Tests...")
    
    # 1. Create User
    user_id = test_create_user()
    if user_id:
        # 2. Try to buy (fail)
        test_initial_buy_fail(user_id)
        
        # 3. Sell to get money (Naive logic test)
        if test_sell_to_add_balance(user_id):
             # 4. Buy with money
             test_buy_with_balance(user_id)
    
    logging.info("Verification Tests Completed.")
