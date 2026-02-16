import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from app.config.database import engine
from sqlalchemy import text

def test_connection():
    try:
        print("Testing database connection...")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Connection successful! Result:", result.scalar())
    except Exception as e:
        print("Connection failed:", e)

if __name__ == "__main__":
    test_connection()
