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

app.include_router(endpoints.router, prefix="/api/v1")

# Background Task Integration
import asyncio
from app.background.scheduler.py import BackgroundMonitor

@app.on_event("startup")
async def startup_event():
    monitor = BackgroundMonitor()
    # Run in background without blocking the server
    asyncio.create_task(monitor.start_monitoring())

@app.get("/")
def read_root():
    return {"message": "Welcome to Stock Project API"}
