from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config.database import SessionLocal

class PortfolioService:
    """
    שירות האחראי על איסוף וניתוח נתוני התיק של המשתמשים.
    מספק שיטות לקבוע אילו מניות מוחזקות כעת באופן פעיל על ידי משתמשים.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_active_holdings(self, user_id: int) -> List[str]:
        """
        מחשב את הכמות נטו הנוכחית של מניות בבעלות משתמש ספציפי.
        מסכם את כל עסקאות הקנייה/מכירה כדי למצוא את היתרה הנוכחית.
        מחזיר רשימה של סמלי מניות שבהם הכמות נטו גדולה מ-0.
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
        מנתח עסקאות של כל המשתמשים כדי למצוא כל מניה ייחודית
        המוחזקת כעת על ידי משתמש אחד לפחות (כמות נטו גדולה מ-0).
        משמש את מנטר הרקע כדי לדעת אילו מניות לעקוב אחריהן.
        מחזיר רשימה של סמלי מניות ייחודיים.
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
