"""
נתב API עבור התראות סנטימנט.

מספק נקודות קצה לשליפה וניהול של התראות מניות בסיכון גבוה
שנוצרו על ידי מערכת הניטור ברקע.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.domain.models import SentimentAlert

router = APIRouter()

@router.get("/alerts", tags=["Alerts"])
def get_alerts(db: Session = Depends(get_db)):
    """
    מושך את כל התראות הסנטימנט בסיכון גבוה ממסד הנתונים,
    ממוינות מהחדשות ביותר לישנות.
    """
    alerts = db.query(SentimentAlert).order_by(SentimentAlert.timestamp.desc()).all()
    return alerts

@router.get("/alerts/unread", tags=["Alerts"])
def get_unread_alerts(db: Session = Depends(get_db)):
    """
    מושך רק התראות סנטימנט בסיכון גבוה שלא נקראו.
    שימושי להצגת התראות למשתמש.
    """
    alerts = db.query(SentimentAlert).filter(SentimentAlert.is_read == 0).order_by(SentimentAlert.timestamp.desc()).all()
    return alerts

@router.post("/alerts/{alert_id}/read", tags=["Alerts"])
def mark_alert_read(alert_id: int, db: Session = Depends(get_db)):
    """
    מסמן התראה ספציפית ככזו שנקראה (אישור קריאת ההתראה).
    """
    alert = db.query(SentimentAlert).filter(SentimentAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_read = 1
    db.commit()
    return {"message": "Alert marked as read"}

