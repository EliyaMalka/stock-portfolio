from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.domain import models
from app.cqrs import commands, queries
from typing import List

class CQRSHandler:
    def __init__(self, db: Session):
        self.db = db

    # Command Handlers
    def handle_create_user(self, command: commands.CreateUserCommand) -> models.User:
        try:
            from passlib.context import CryptContext
            # Switching to argon2 to avoid 72 byte limit of bcrypt and for better security
            pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
            hashed_password = pwd_context.hash(command.Password)
        except Exception as e:
            print(f"Hashing Error: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Hashing failed: {str(e)}")

        db_user = models.User(
            Username=command.Username, 
            Email=command.Email,
            HashedPassword=hashed_password,
            Balance=0.00
        )
        try:
            self.db.add(db_user)
            self.db.commit()
            print("Committed user to DB")
            self.db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            self.db.rollback()
            print(f"Integrity Error: {e}")
            raise HTTPException(status_code=400, detail="Username or Email already exists")
            print(f"DB Error: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def handle_login(self, command: commands.LoginUserCommand) -> models.User:
        db_user = self.db.query(models.User).filter(models.User.Username == command.Username).first()
        if not db_user:
             raise HTTPException(status_code=401, detail="Invalid username or password")
        
        try:
             from passlib.context import CryptContext
             pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
             if not pwd_context.verify(command.Password, db_user.HashedPassword):
                 raise HTTPException(status_code=401, detail="Invalid username or password")
        except Exception as e:
            print(f"Login Verify Error: {e}")
            raise HTTPException(status_code=500, detail="Authentication failed")
        
        return db_user

    def handle_update_user(self, command: commands.UpdateUserCommand) -> models.User:
        db_user = self.db.query(models.User).filter(models.User.UserID == command.UserID).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db_user.Username = command.Username
        db_user.Email = command.Email
        
        try:
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Username or Email already exists")

    def handle_delete_user(self, command: commands.DeleteUserCommand):
        db_user = self.db.query(models.User).filter(models.User.UserID == command.UserID).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        self.db.delete(db_user)
        self.db.commit()
        return {"detail": "User deleted successfully"}

    def handle_create_transaction(self, command: commands.CreateTransactionCommand) -> models.Transaction:
        user = self.db.query(models.User).filter(models.User.UserID == command.UserID).first()
        if not user:
             raise HTTPException(status_code=404, detail="User not found")

        total_amount = command.Quantity * command.PricePerStock

        # Handle Balance Logic
        if command.Quantity > 0: # Buy
            if user.Balance < total_amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")
            user.Balance -= total_amount
        elif command.Quantity < 0: # Sell (Quantity is negative, so total_amount is negative)
            # Check if user has enough stock to sell
            transactions = self.db.query(models.Transaction).filter(
                models.Transaction.UserID == command.UserID,
                models.Transaction.StockSymbol == command.StockSymbol
            ).all()
            
            current_holdings = sum(t.Quantity for t in transactions)
            
            # command.Quantity is negative, so current_holdings + command.Quantity must be >= 0
            if current_holdings + command.Quantity < 0:
                raise HTTPException(status_code=400, detail=f"Insufficient stock holdings. You have {current_holdings} shares of {command.StockSymbol}.")

            # Subtracting a negative number adds to the balance
            user.Balance -= total_amount 
        
        # Note: If Quantity is 0, nothing happens to balance (though 0 quantity transactions might be weird, we don't block them here based on SQL constraint removal)

        db_transaction = models.Transaction(
            UserID=command.UserID,
            StockSymbol=command.StockSymbol,
            Quantity=command.Quantity,
            PricePerStock=command.PricePerStock
        )
        
        try:
            self.db.add(db_transaction)
            self.db.commit() # Commit transaction and user balance update atomically
            self.db.refresh(db_transaction)
            return db_transaction
        except Exception as e:
            self.db.rollback()
            print(f"Transaction Error: {e}")
            raise HTTPException(status_code=500, detail=f"Transaction failed: {str(e)}")

    # Query Handlers
    def handle_get_user(self, query: queries.GetUserQuery) -> models.User:
        user = self.db.query(models.User).filter(models.User.UserID == query.UserID).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def handle_get_all_users(self, query: queries.GetAllUsersQuery) -> List[models.User]:
        return self.db.query(models.User).all()

    def handle_get_transaction(self, query: queries.GetTransactionQuery) -> models.Transaction:
        transaction = self.db.query(models.Transaction).filter(models.Transaction.TransactionID == query.TransactionID).first()
        if not transaction:
             raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    
    def handle_get_user_transactions(self, query: queries.GetUserTransactionsQuery) -> List[models.Transaction]:
        return self.db.query(models.Transaction).filter(models.Transaction.UserID == query.UserID).all()
