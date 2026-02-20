"""
פקודות CQRS.

מבני נתונים המייצגים כוונה לשנות מצב (Create, Update, Delete).
מועברים מהנתבים (routers) ל-CQRSHandler לביצוע.
"""
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class CreateUserCommand:
    Username: str
    Email: str
    Password: str

@dataclass
class UpdateUserCommand:
    UserID: int
    Username: str
    Email: str

@dataclass
class DeleteUserCommand:
    UserID: int

@dataclass
class CreateTransactionCommand:
    UserID: int
    StockSymbol: str
    Quantity: int
    PricePerStock: Decimal

@dataclass
class LoginUserCommand:
    Username: str
    Password: str

