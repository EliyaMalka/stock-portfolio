from pydantic import BaseModel, EmailStr, condecimal, Field
from typing import List, Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    Username: str = Field(..., max_length=50)
    Email: EmailStr

class UserCreate(UserBase):
    Password: str = Field(..., min_length=6)

class UserUpdate(UserBase):
    pass

class UserRead(UserBase):
    UserID: int
    Balance: condecimal(max_digits=18, decimal_places=2)
    
    class Config:
        from_attributes = True

# Transaction Schemas
class TransactionBase(BaseModel):
    StockSymbol: str = Field(..., max_length=10)
    Quantity: int = Field(...)  # Removed gt=0 to allow selling
    PricePerStock: condecimal(max_digits=18, decimal_places=2)

class TransactionCreate(TransactionBase):
    UserID: int

class TransactionRead(TransactionBase):
    TransactionID: int
    UserID: int
    TransactionDate: datetime

    class Config:
        from_attributes = True

class UserWithTransactions(UserRead):
    transactions: List[TransactionRead] = []

class UserLogin(BaseModel):
    Username: str = Field(..., max_length=50)
    Password: str = Field(..., min_length=1) # Allow any length for now, or match registration policy
