"""
מודלי ליבה (Domain Models) של האפליקציה.

מגדיר את מודלי ה-ORM של SQLAlchemy המייצגים את טבלאות מסד הנתונים
עבור Users, Transactions ו-Sentiment Alerts.
"""
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

class User(Base):
    """
    מייצג משתמש רשום במערכת.
    מאחסן פרטי התחברות (מגובבים) ואת יתרת החשבון הנוכחית.
    בעל קשר יחיד-לרבים (one-to-many) עם עסקאות (Transactions).
    """
    __tablename__ = "Users"

    UserID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Username = Column(String(50), unique=True, nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    HashedPassword = Column(String(255), nullable=False)
    Balance = Column(DECIMAL(18, 2), default=0.00)

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

class Transaction(Base):
    """
    מייצג עסקת קנייה/מכירה של מניות.
    כמות חיובית מרמזת על רכישה; כמות שלילית מרמזת על מכירה.
    מקושר למשתמש ספציפי באמצעות UserID.
    """
    __tablename__ = "Transactions"

    TransactionID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("Users.UserID"), nullable=False)
    StockSymbol = Column(String(10), nullable=False)
    Quantity = Column(Integer, nullable=False)
    PricePerStock = Column(DECIMAL(18, 2), nullable=False)
    TransactionDate = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")

class SentimentAlert(Base):
    """
    מייצג התראה שנוצרה על ידי מנטר הסיכונים ברקע.
    מאחסן כותרות חדשות שליליות ואת ציוני הסנטימנט המשויכים אליהן
    עבור מניות המוחזקות על ידי משתמשים.
    """
    __tablename__ = "SentimentAlerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    stock_symbol = Column(String(10), nullable=False)
    sentiment_score = Column(DECIMAL(10, 4), nullable=False)
    headline = Column(String(500), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Integer, default=0) # Using Integer as boolean (0/1) for wide compatibility if needed, or Boolean

