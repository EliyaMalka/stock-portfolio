from fastapi import FastAPI
from app.config.database import engine, Base
from app.api import endpoints

"""
נקודת הכניסה הראשית של אפליקציית FastAPI.

מודול זה מאתחל את השרת, מגדיר את נתיבי ה-API,
ומגדיר משימות רקע כמו ניטור סיכוני סנטימנט.
"""

# Create tables if they don't exist (though they likely do)
# Base.metadata.create_all(bind=engine) 

app = FastAPI(
    title="Stock Project API",
    description="CQRS based FastAPI server for Stock Project",
    version="1.0.0"
)

from app.routers import users, transactions, alerts, sentiment

# Include all application routers under the /api/v1 prefix
app.include_router(users.router, prefix="/api/v1")
app.include_router(transactions.router, prefix="/api/v1")
app.include_router(alerts.router, prefix="/api/v1")
app.include_router(sentiment.router, prefix="/api/v1")

# Background Task Integration
import asyncio
from app.background.scheduler import BackgroundMonitor

@app.on_event("startup")
async def startup_event():
    """
    מטפל באירוע הפעלת האפליקציה.
    אחראי על אתחול טבלאות מסד הנתונים והפעלת משימות רקע אסינכרוניות,
    כגון שירות ניטור סיכוני התיק.
    """
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
    """
    נקודת קצה לבדיקת תקינות (Health check).
    מחזירה הודעת ברוכים הבאים כדי לאשר שה-API פועל בהצלחה.
    """
    return {"message": "Welcome to Stock Project API"}
