import requests
import random
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

# Sample Data
USERS = [
    {"Username": "john_doe", "Email": "john@example.com", "Password": "password123"},
    {"Username": "jane_smith", "Email": "jane@example.com", "Password": "securePass!23"},
    {"Username": "mike_ross", "Email": "mike@example.com", "Password": "suitsFan101"},
    {"Username": "rachel_zane", "Email": "rachel@example.com", "Password": "paralegalLife"},
    {"Username": "harvey_specter", "Email": "harvey@example.com", "Password": "closerTheBest"}
]

STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "TSMC", "NVDA", "META"]

def create_users():
    created_users = []
    print("--- Creating Users ---")
    for user in USERS:
        try:
            print(f"Creating {user['Username']}...")
            response = requests.post(f"{BASE_URL}/users", json=user)
            if response.status_code == 201:
                created_user = response.json()
                created_users.append(created_user)
                print(f"  Success! ID: {created_user['UserID']}")
            elif response.status_code == 400:
                print(f"  User {user['Username']} already exists. Fetching details...")
                # Try to login to get the ID if we can't create
                login_response = requests.post(f"{BASE_URL}/login", json={"Username": user['Username'], "Password": user['Password']})
                if login_response.status_code == 200:
                    created_users.append(login_response.json())
                    print("  Retrieved existing ID.")
                else:
                    print("  Could not retrieve ID.")
            else:
                print(f"  Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"  Error: {e}")
    return created_users

def create_transactions(users):
    print("\n--- Creating Transactions ---")
    if not users:
        print("No users to add transactions to.")
        return

    for user in users:
        user_id = user['UserID']
        num_transactions = 5
        print(f"Adding {num_transactions} transactions for User ID {user_id} ({user['Username']})...")
        
        for _ in range(num_transactions):
            stock = random.choice(STOCKS)
            quantity = random.randint(1, 20)
            price = round(random.uniform(100.0, 500.0), 2)
            
            # Simple logic: mostly buys, some sells if they have stock (simplified here to just random buys/sells)
            # To ensure they have balance, let's just do buys properly or handled by server logic.
            # Server logic handles balance checks. New users have 0 balance.
            # Wait, if balance is 0, they can't buy! 
            # We need to give them money first or just force transactions?
            # The server enforces balance. 
            # Workaround: Sell some fake stock to get money? Or maybe the initial user creation should give bonus?
            # Or just "Sell" a stock they don't have? (Short selling? No, server checks quantity... wait, server check `get_user_stock_quantity` is in client view logic, server handler logic is: )
            
            # Server Handler Logic (from handlers.py):
            # if Quantity > 0 (Buy): if Balance < cost => Error
            # if Quantity < 0 (Sell): Balance += revenue.
            # It DOES NOT check if they own the stock on the server side in `handle_create_transaction`.
            # So we can "Sell" to generate funds.
            
            # Strategy: Sell a high value stock first to get balance, then buy some randoms.
            
            # 1. Deposit money (via "Selling" a stock they magically exist, since server doesn't validate ownership quantity yet for sells, only Client does)
            
            # Action: Sell 100 shares of AAPL at $150 (Total +$15,000)
            deposit_transaction = {
                "UserID": user_id,
                "StockSymbol": "CASH_DEPOSIT", 
                "Quantity": -100, 
                "PricePerStock": 100.00 
            }
            requests.post(f"{BASE_URL}/transactions", json=deposit_transaction) 

            # Now real transactions
            transaction = {
                "UserID": user_id,
                "StockSymbol": stock,
                "Quantity": quantity, # Buy
                "PricePerStock": price
            }
            
            res = requests.post(f"{BASE_URL}/transactions", json=transaction)
            if res.status_code == 201:
                print(f"  Bought {quantity} {stock} at ${price}")
            else:
                print(f"  Failed to buy: {res.text}")

if __name__ == "__main__":
    users = create_users()
    create_transactions(users)
    print("\nDone!")
