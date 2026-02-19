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
)

# Using pymssql as a fallback because the installed ODBC driver is too old for pyodbc + SQLAlchemy 2.0
# and throws "Invalid precision value" errors.
# We construct the URL manually for pymssql
db_server = os.getenv('DB_SERVER')
db_name = os.getenv('DB_NAME')
db_uid = os.getenv('DB_UID')
db_pwd = os.getenv('DB_PWD')

# pymssql format: mssql+pymssql://<username>:<password>@<host>/<dbname>
DATABASE_URL = f"mssql+pymssql://{db_uid}:{db_pwd}@{db_server}/{db_name}"

engine = create_engine(DATABASE_URL, echo=True)

# Event listeners for pyodbc are typically not needed for pymssql 
# unless encoding issues arise (pymssql usually handles UTF-8 well by default)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
