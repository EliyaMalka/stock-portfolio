# Stock Portfolio Application

A comprehensive, full-stack application for managing a simulated stock portfolio, featuring a CQRS backend architecture and an interactive Windows desktop client with AI assistance capabilities.

## Project Structure

The project is split into two primary components:

### 1. FastAPI Backend (`fastapi/`)

A robust API server built with FastAPI using a Command Query Responsibility Segregation (CQRS) pattern. It manages the core business logic, user accounts, transactions, and portfolio risk evaluation.

- **Stack**: FastAPI, SQLAlchemy, SQLAlchemy ORM, SQLite (default).
- **Features**: User authentication, stock market data fetching via `yfinance`, FinBERT-based sentiment analysis, background risk monitoring, and granular transaction tracking.

See the [Backend README](fastapi/README.md) for detailed architectural documentation.

### 2. Windows GUI Client (`windows systerm project-python/`)

A rich desktop application built with PySide6, providing a user-friendly interface to interact with the portfolio backend.

- **Stack**: Python, PySide6, Matplotlib, Langchain/LangGraph.
- **Features**: Real-time stock charting, transaction management (buy/sell), user profile management, and an integrated AI financial assistant capable of querying real-time prices and executing trades directly.

See the [Frontend README](windows%20systerm%20project-python/README.md) for detailed client architecture.

## Getting Started

### Prerequisites

- Python 3.10+
- (Optional but recommended) Ollama running locally for the AI reasoning agent.

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd stock-portfolio
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   *(Ideally, install from `requirements.txt` if available. Otherwise, the main dependencies are listed below)*
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic passlib[bcrypt] yfinance transformers torch PySide6 matplotlib pandas langchain langgraph
   ```

### Running the Application

Both components need to run simultaneously. It's recommended to open two separate terminal windows.

**Terminal 1: Start the Backend Server**
```bash
cd fastapi
uvicorn app.main:app --reload --port 8000
```
The API will be available at `http://localhost:8000`. You can access the automatic Swagger documentation at `http://localhost:8000/docs`.

**Terminal 2: Start the Desktop Client**
```bash
cd "windows systerm project-python"
python main.py
```
This will launch the desktop GUI. You can register a new user or log in with existing credentials to start managing the simulated portfolio.
