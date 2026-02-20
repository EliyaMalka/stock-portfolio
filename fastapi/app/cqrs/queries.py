"""
CQRS Queries.

Data structures representing requests for information without mutating state.
These are passed from routers to the CQRSHandler to fetch data.
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

