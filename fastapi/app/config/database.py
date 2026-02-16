from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection parameters
params = urllib.parse.quote_plus(
    f"DRIVER={os.getenv('DB_DRIVER')};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_UID')};"
    f"PWD={os.getenv('DB_PWD')};"
    f"TrustServerCertificate={os.getenv('DB_TRUST_CERT')};"
)

DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
