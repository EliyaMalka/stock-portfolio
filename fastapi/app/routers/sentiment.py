"""
נתב API עבור ניתוח סנטימנט.

מספק נקודות קצה לפי דרישה לניתוח סנטימנט השוק הנוכחי
עבור סמלי מניות ספציפיים בהתבסס על כותרות חדשות אחרונות.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.services.news_service import NewsService
from app.services.sentiment_service import SentimentService

router = APIRouter()

# Instantiate services (could be improved with dependency injection)
news_service = NewsService()
sentiment_service = SentimentService()

class SentimentRequest(BaseModel):
    """סכימה עבור בקשת ניתוח סנטימנט."""
    symbol: str

class SentimentResponse(BaseModel):
    """סכימה עבור תוצאות ניתוח סנטימנט."""
    symbol: str
    overall_sentiment: str # Positive, Negative, Neutral
    average_score: float
    headlines: List[str]

@router.post("/sentiment/analyze", tags=["Sentiment"], response_model=SentimentResponse)
def analyze_sentiment(request: SentimentRequest):
    """
    מבצע ניתוח סנטימנט לפי דרישה עבור מניה ספציפית.
    מושך את כותרות החדשות העדכניות ביותר, מחשב את ציוני הסנטימנט שלהן,
    ומחזיר קריאת סנטימנט כוללת מסוכמת.
    """
    symbol = request.symbol.upper()
    
    # 1. Fetch News
    try:
        # fetch_news expects a list of tickers
        news_data = news_service.fetch_news([symbol])
        headlines = news_data.get(symbol, [])
        
        if not headlines:
            return SentimentResponse(
                symbol=symbol,
                overall_sentiment="Neutral (No News)",
                average_score=0.0,
                headlines=[]
            )
            
        # 2. Analyze Sentiment
        total_score = 0.0
        analyzed_count = 0
        
        for headline in headlines:
            score = sentiment_service.analyze(headline)
            total_score += score
            analyzed_count += 1
            
        avg_score = total_score / analyzed_count if analyzed_count > 0 else 0.0
        
        # Determine label
        if avg_score > 0.2:
            sentiment = "Positive"
        elif avg_score < -0.2:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
            
        return SentimentResponse(
            symbol=symbol,
            overall_sentiment=sentiment,
            average_score=avg_score,
            headlines=headlines[:3] # Return top 3 headlines
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

