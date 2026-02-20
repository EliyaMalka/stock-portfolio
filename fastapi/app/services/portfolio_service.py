from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config.database import SessionLocal

class PortfolioService:
    """
    Service responsible for aggregating and analyzing user portfolio data.
    Provides methods to determine which stocks are currently actively held by users.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_active_holdings(self, user_id: int) -> List[str]:
        """
        Calculates the current net quantity of stocks owned by a specific user.
        Aggregates all buy/sell transactions to find the current balance.
        Returns a list of ticker symbols where the net quantity is > 0.
        """
        query = text("SELECT StockSymbol, Quantity FROM Transactions WHERE UserID = :user_id")
        result = self.db.execute(query, {"user_id": user_id}).fetchall()

        holdings: Dict[str, int] = {}

        for row in result:
            symbol = row.StockSymbol
            qty = row.Quantity
            
            if symbol in holdings:
                holdings[symbol] += qty
            else:
                holdings[symbol] = qty

        # Filter for stocks with positive quantity
        active_tickers = [symbol for symbol, qty in holdings.items() if qty > 0]
        return active_tickers

    def get_all_active_stocks(self) -> List[str]:
        """
        Analyzes transactions across all users to find every unique stock 
        currently held by at least one user (net quantity > 0).
        Used by the background monitor to know which stocks to track.
        Returns a list of unique ticker symbols.
        """
        # Fetch all transactions
        query = text("SELECT UserID, StockSymbol, Quantity FROM Transactions")
        result = self.db.execute(query).fetchall()

        # Track holdings per user to correctly net off buys/sells
        user_holdings: Dict[int, Dict[str, int]] = {}

        for row in result:
            uid = row.UserID
            symbol = row.StockSymbol
            qty = row.Quantity
            
            if uid not in user_holdings:
                user_holdings[uid] = {}
            
            if symbol in user_holdings[uid]:
                user_holdings[uid][symbol] += qty
            else:
                user_holdings[uid][symbol] = qty

        # Collect all unique tickers with positive quantity from any user
        active_tickers_set = set()
        for uid, holdings in user_holdings.items():
            for symbol, qty in holdings.items():
                if qty > 0:
                    active_tickers_set.add(symbol)
        
        return list(active_tickers_set)
