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
