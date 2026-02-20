"""
נתב API עבור ניהול משתמשים.

מספק נקודות קצה ליצירה, אימות, שליפה, עדכון,
ומחיקה של משתמשים, כמו גם ניהול יתרות החשבון שלהם.
מנתב פקודות ושאילתות דרך מנהל ה-CQRS.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.domain import schemas
from app.cqrs import commands, queries
from app.cqrs.handlers import CQRSHandler

router = APIRouter()

def get_handler(db: Session = Depends(get_db)) -> CQRSHandler:
    """ספק תלויות המזריק את סשן מסד הנתונים לתוך CQRSHandler."""
    return CQRSHandler(db)

# User Endpoints
@router.post("/users", response_model=schemas.UserRead, status_code=201)
def create_user(user: schemas.UserCreate, handler: CQRSHandler = Depends(get_handler)):
    """
    רושם משתמש חדש במערכת.
    מצפה ל-Username, Email ו-Password. יוצר CreateUserCommand.
    """
    command = commands.CreateUserCommand(
        Username=user.Username, 
        Email=user.Email,
        Password=user.Password
    )
    return handler.handle_create_user(command)

@router.post("/login", response_model=schemas.UserRead, status_code=200)
def login_user(user: schemas.UserLogin, handler: CQRSHandler = Depends(get_handler)):
    """
    מאמת משתמש.
    מוודא את ה-Username וה-Password שסופקו מול הגיבוב (hash) השמור.
    מחזיר פרטי משתמש במקרה של הצלחה.
    """
    command = commands.LoginUserCommand(
        Username=user.Username,
        Password=user.Password
    )
    return handler.handle_login(command)

@router.get("/users", response_model=List[schemas.UserRead])
def get_users(handler: CQRSHandler = Depends(get_handler)):
    """
    שולף רשימה של כל המשתמשים הרשומים.
    מבצע GetAllUsersQuery.
    """
    query = queries.GetAllUsersQuery()
    return handler.handle_get_all_users(query)

@router.get("/users/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, handler: CQRSHandler = Depends(get_handler)):
    """
    שולף את הפרטים של משתמש ספציפי לפי ה-ID שלו.
    מבצע GetUserQuery.
    """
    query = queries.GetUserQuery(UserID=user_id)
    return handler.handle_get_user(query)

@router.put("/users/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, user: schemas.UserUpdate, handler: CQRSHandler = Depends(get_handler)):
    """
    מעדכן את ה-Username ו/או ה-Email של משתמש קיים.
    מבצע UpdateUserCommand.
    """
    command = commands.UpdateUserCommand(UserID=user_id, Username=user.Username, Email=user.Email)
    return handler.handle_update_user(command)

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, handler: CQRSHandler = Depends(get_handler)):
    """
    מוחק משתמש ואת העסקאות המשויכות אליו ממסד הנתונים.
    מבצע DeleteUserCommand.
    """
    command = commands.DeleteUserCommand(UserID=user_id)
    handler.handle_delete_user(command)
    return

# Balance Management Endpoints
class BalanceUpdate(schemas.BaseModel):
    amount: float

@router.post("/users/{user_id}/balance/add", response_model=schemas.UserRead)
def add_balance(user_id: int, update: BalanceUpdate, handler: CQRSHandler = Depends(get_handler)):
    from app.domain.models import User
    from decimal import Decimal
    
    user = handler.db.query(User).filter(User.UserID == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.Balance += Decimal(str(update.amount))
    handler.db.commit()
    handler.db.refresh(user)
    return user

@router.post("/users/{user_id}/balance/withdraw", response_model=schemas.UserRead)
def withdraw_balance(user_id: int, update: BalanceUpdate, handler: CQRSHandler = Depends(get_handler)):
    from app.domain.models import User
    from decimal import Decimal
    
    user = handler.db.query(User).filter(User.UserID == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    amount_decimal = Decimal(str(update.amount))
    if user.Balance < amount_decimal:
        raise HTTPException(status_code=400, detail="Insufficient funds")
        
    user.Balance -= amount_decimal
    handler.db.commit()
    handler.db.refresh(user)
    return user
