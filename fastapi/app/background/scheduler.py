import asyncio
from app.services.portfolio_service import PortfolioService
from app.services.news_service import NewsService
from app.services.sentiment_service import SentimentService
from app.config.database import SessionLocal

class BackgroundMonitor:
    def __init__(self):
        self.news_service = NewsService()
        self.sentiment_service = SentimentService() # Will load model on first init
    
    async def start_monitoring(self):
        # Allow the server to start up fully before heavy loading
        await asyncio.sleep(10) 
        print("Starting Background Risk Monitor...")
        
        while True:
            try:
                # 1. Get Active Stocks
                db = SessionLocal()
                # For this example, we'll check for User ID 4 (the active user in your flow)
                # In a real app, you'd loop through all users or unique stocks
                active_tickers = PortfolioService(db).get_active_holdings(user_id=4)
                db.close()

                if not active_tickers:
                    print("No active stocks found to monitor.")
                else:
                    print(f"Monitoring stocks: {active_tickers}")
                    
                    # 2. Get News
                    news_data = self.news_service.fetch_news(active_tickers)
                    
                    # 3. Analyze Risks
                    for ticker, headlines in news_data.items():
                        for headline in headlines:
                            score = self.sentiment_service.analyze(headline)
                            
                            # Log risk if significantly negative
                            if score < -0.7:
                                print(f"⚠️ [RISK ALERT] {ticker}: Sentiment {score:.2f} | Headline: {headline}")
                                # TODO: Save this alert to DB for the Agent to pick up
                            elif score > 0.7:
                                print(f"✅ [OPPORTUNITY] {ticker}: Sentiment {score:.2f} | Headline: {headline}")

            except Exception as e:
                print(f"Error in background monitor: {e}")

            # Wait 15 minutes before next scan (900 seconds)
            # Shortened to 60s for demo purposes
            await asyncio.sleep(60)
