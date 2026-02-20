# Stock Portfolio FastAPI Backend

This directory contains the backend services for the Stock Portfolio application, built with FastAPI. It provides the RESTful API endpoints used by the Windows client for user management, stock transactions, sentiment analysis, and risk alerts.

## Architecture

The backend follows a **CQRS (Command Query Responsibility Segregation)** pattern combined with a Domain-Driven Design (DDD) approach. This structure separates the logic for reading data (Queries) from the logic for mutating data (Commands).

### Directory Structure

- **`app/main.py`**: The entry point of the FastAPI application. Initializes the server, configures routers, and starts background tasks.
- **`app/routers/`**: Contains the API endpoints. They receive HTTP requests and route them to the appropriate services or CQRS handlers.
    - `users.py`: Registration, login, and balance management.
    - `transactions.py`: Buying and selling stocks.
    - `sentiment.py`: On-demand FinBERT sentiment analysis.
    - `alerts.py`: Fetching and acknowledging high-risk portfolio alerts.
- **`app/cqrs/`**: Implements the CQRS pattern.
    - `commands.py`: Data classes representing actions that change state (e.g., `CreateUserCommand`).
    - `queries.py`: Data classes representing requests for data (e.g., `GetUserQuery`).
    - `handlers.py`: The `CQRSHandler` class containing the business logic to execute Commands and Queries against the database.
- **`app/domain/`**: Contains data representations.
    - `models.py`: SQLAlchemy ORM models mapping to database tables (`Users`, `Transactions`, `SentimentAlerts`).
    - `schemas.py`: Pydantic models used by FastAPI for request validation and response serialization.
- **`app/services/`**: Encapsulates external integrations and complex logic.
    - `news_service.py`: Fetches news from Yahoo Finance.
    - `sentiment_service.py`: Uses a Hugging Face FinBERT model to analyze text sentiment.
    - `portfolio_service.py`: Calculates active stock holdings for users.
- **`app/background/`**: Background tasks.
    - `scheduler.py`: Contains the `BackgroundMonitor` that periodically checks user portfolios for negative news.
- **`app/config/`**: Configuration files (e.g., database connection setup).

## Setup & Running

1. Create and activate a Python virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
4. Access the interactive API documentation at `http://localhost:8000/docs`.
