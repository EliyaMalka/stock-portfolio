"""
API Router for Transactions.

Provides endpoints for creating stock buy/sell transactions and retrieving
transaction history for specific transactions or users.
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
    """Dependency provider injecting the database session into the CQRSHandler."""
    return CQRSHandler(db)

# Transaction Endpoints
@router.post("/transactions", response_model=schemas.TransactionRead, status_code=201)
def create_transaction(transaction: schemas.TransactionCreate, handler: CQRSHandler = Depends(get_handler)):
    """
    Records a new stock transaction (buy or sell).
    Executes CreateTransactionCommand.
    """
    command = commands.CreateTransactionCommand(
        UserID=transaction.UserID,
        StockSymbol=transaction.StockSymbol,
        Quantity=transaction.Quantity,
        PricePerStock=transaction.PricePerStock
    )
    return handler.handle_create_transaction(command)

@router.get("/transactions/{transaction_id}", response_model=schemas.TransactionRead)
def get_transaction(transaction_id: int, handler: CQRSHandler = Depends(get_handler)):
    """
    Retrieves the details of a specific transaction by its ID.
    Executes GetTransactionQuery.
    """
    query = queries.GetTransactionQuery(TransactionID=transaction_id)
    return handler.handle_get_transaction(query)

@router.get("/users/{user_id}/transactions", response_model=List[schemas.TransactionRead])
def get_user_transactions(user_id: int, handler: CQRSHandler = Depends(get_handler)):
    """
    Retrieves all transactions associated with a specific user.
    Executes GetUserTransactionsQuery.
    """
    query = queries.GetUserTransactionsQuery(UserID=user_id)
    return handler.handle_get_user_transactions(query)

