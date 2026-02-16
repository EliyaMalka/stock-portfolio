from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.domain import schemas
from app.cqrs import commands, queries
from app.cqrs.handlers import CQRSHandler

router = APIRouter()

def get_handler(db: Session = Depends(get_db)) -> CQRSHandler:
    return CQRSHandler(db)

# User Endpoints
@router.post("/users", response_model=schemas.UserRead, status_code=201)
def create_user(user: schemas.UserCreate, handler: CQRSHandler = Depends(get_handler)):
    command = commands.CreateUserCommand(
        Username=user.Username, 
        Email=user.Email,
        Password=user.Password
    )
    return handler.handle_create_user(command)

@router.post("/login", response_model=schemas.UserRead, status_code=200)
def login_user(user: schemas.UserLogin, handler: CQRSHandler = Depends(get_handler)):
    command = commands.LoginUserCommand(
        Username=user.Username,
        Password=user.Password
    )
    return handler.handle_login(command)

@router.get("/users", response_model=List[schemas.UserRead])
def get_users(handler: CQRSHandler = Depends(get_handler)):
    query = queries.GetAllUsersQuery()
    return handler.handle_get_all_users(query)

@router.get("/users/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, handler: CQRSHandler = Depends(get_handler)):
    query = queries.GetUserQuery(UserID=user_id)
    return handler.handle_get_user(query)

@router.put("/users/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, user: schemas.UserUpdate, handler: CQRSHandler = Depends(get_handler)):
    command = commands.UpdateUserCommand(UserID=user_id, Username=user.Username, Email=user.Email)
    return handler.handle_update_user(command)

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, handler: CQRSHandler = Depends(get_handler)):
    command = commands.DeleteUserCommand(UserID=user_id)
    handler.handle_delete_user(command)
    return

# Transaction Endpoints
@router.post("/transactions", response_model=schemas.TransactionRead, status_code=201)
def create_transaction(transaction: schemas.TransactionCreate, handler: CQRSHandler = Depends(get_handler)):
    command = commands.CreateTransactionCommand(
        UserID=transaction.UserID,
        StockSymbol=transaction.StockSymbol,
        Quantity=transaction.Quantity,
        PricePerStock=transaction.PricePerStock
    )
    return handler.handle_create_transaction(command)

@router.get("/transactions/{transaction_id}", response_model=schemas.TransactionRead)
def get_transaction(transaction_id: int, handler: CQRSHandler = Depends(get_handler)):
    query = queries.GetTransactionQuery(TransactionID=transaction_id)
    return handler.handle_get_transaction(query)

@router.get("/users/{user_id}/transactions", response_model=List[schemas.TransactionRead])
def get_user_transactions(user_id: int, handler: CQRSHandler = Depends(get_handler)):
    query = queries.GetUserTransactionsQuery(UserID=user_id)
    return handler.handle_get_user_transactions(query)
