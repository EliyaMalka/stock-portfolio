from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config.database import SessionLocal

class PortfolioService:
    def __init__(self, db: Session):
        self.db = db

    def get_active_holdings(self, user_id: int) -> List[str]:
        """
        Calculates the current quantity of stocks owned by the user.
        Returns a list of ticker symbols where the quantity is > 0.
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
