import yfinance as yf
from typing import List, Dict

class NewsService:
    """
    שירות האחראי על הבאת החדשות הפיננסיות העדכניות ביותר.
    משתמש בספריית yfinance לשליפת כותרות חדשות עבור סמלי מניות ספציפיים.
    """
    def fetch_news(self, tickers: List[str]) -> Dict[str, List[str]]:
        """
        מושך את כותרות החדשות העדכניות ביותר עבור סמלי המניות הנתונים.
        מחזיר מילון: { "AAPL": ["Headline 1", "Headline 2"], ... }
        """
        news_data = {}
        
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                # yfinance returns a list of dictionaries with 'title', 'link', etc.
                raw_news = stock.news
                
                headlines = []
                if raw_news:
                    # Get top 3 headlines to save processing time
                    for item in raw_news[:3]:
                        headlines.append(item.get('title', ''))
                
                if headlines:
                    news_data[ticker] = headlines
                    
            except Exception as e:
                print(f"Error fetching news for {ticker}: {e}")
                
        return news_data
