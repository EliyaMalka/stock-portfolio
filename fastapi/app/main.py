from fastapi import FastAPI
from app.config.database import engine, Base
from app.api import endpoints

# Create tables if they don't exist (though they likely do)
# Base.metadata.create_all(bind=engine) 

app = FastAPI(
    title="Stock Project API",
    description="CQRS based FastAPI server for Stock Project",
    version="1.0.0"
)

from app.routers import users, transactions, alerts, sentiment

app.include_router(users.router, prefix="/api/v1")
app.include_router(transactions.router, prefix="/api/v1")
app.include_router(alerts.router, prefix="/api/v1")
app.include_router(sentiment.router, prefix="/api/v1")

# Background Task Integration
import asyncio
from app.background.scheduler import BackgroundMonitor

@app.on_event("startup")
async def startup_event():
    # Ensure tables are created
    # In production, use migrations (Alembic). For dev, this is fine.
    # We need to import the model so Base knows about it
    from app.domain.models import SentimentAlert, Base
    Base.metadata.create_all(bind=engine)
    
    monitor = BackgroundMonitor()
    # Run in background without blocking the server
    asyncio.create_task(monitor.start_monitoring())

@app.get("/")
def read_root():
    return {"message": "Welcome to Stock Project API"}
