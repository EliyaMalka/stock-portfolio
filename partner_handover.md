# Sentiment Analysis Service - Handover Note

## Overview
We have implemented a background service in the FastAPI backend that uses **FinBERT** (a financial-specific BERT model) to analyze news sentiment for stocks owned by the user.

## What Has Been Done
1.  **Dependencies**: Added `transformers`, `torch`, and `yfinance` to `fastapi/requirements.txt`.
2.  **Portfolio Service**: Created `app/services/portfolio_service.py` to calculate active holdings from the transaction history (ignoring sold stocks).
3.  **News Fetcher**: Created `app/services/news_service.py` to fetch recent headlines for specific tickers using `yfinance`.
4.  **Sentiment Engine**: Created `app/services/sentiment_service.py` that loads `ProsusAI/finbert`. It exposes an `analyze(text)` method returning a float score (-1.0 to 1.0).
5.  **Background Monitor**: Implemented a loop in `app/background/scheduler.py` that runs every 15 minutes. It:
    *   Gets the user's active stocks.
    *   Fetches news for them.
    *   Calculates sentiment.
    *   **CRITICAL**: If sentiment is `< -0.7` (Strong Negative), it logs a "SELL SIGNAL".

## What Is Left To Do (For You/LangChain)
1.  **Database Hook**: Currently, the "SELL SIGNAL" is just printed/logged. You need to decide where to store this for your Agent to see (e.g., a `SentimentAlerts` table in SQL or a shared in-memory dictionary).
2.  **Agent Integration**: Your LangChain agent needs a Tool/Function to query this data.
    *   *Example Tool Name*: `get_risk_alerts(user_id)`
    *   *Logic*: If the tool returns a high-risk alert for a stock the user owns, the Agent should proactively message the user: *"Warning: Heavy negative news detected for [Stock]. FinBERT Score: -0.92."*

## Technical Note
The FinBERT model is heavy (~400MB). On the first run, the server will take a moment to download it. Ensure your machine has internet access during the first start.
