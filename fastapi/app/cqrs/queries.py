"""
שאילתות CQRS.

מבני נתונים המייצגים בקשות למידע ללא שינוי מצב.
מועברים מהנתבים (routers) ל-CQRSHandler לשליפת נתונים.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class GetUserQuery:
    UserID: int

@dataclass
class GetAllUsersQuery:
    pass

@dataclass
class GetTransactionQuery:
    TransactionID: int

@dataclass
class GetUserTransactionsQuery:
    UserID: int

