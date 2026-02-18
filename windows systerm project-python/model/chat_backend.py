import requests
import yfinance as yf
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

# Using LangGraph components
from langgraph.prebuilt import create_react_agent

import model.user as user_model

# === Configuration ===
OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama3.2" 

COLLECTION_NAME = "stock_qa_collection"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
TOP_K = 3
API_URL = "http://localhost:8000/api/v1"

# === Setup ===
# Qdrant for RAG
try:
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    embedder = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
except Exception as e:
    print(f"Warning: Qdrant/Embedder init failed: {e}")
    client = None
    embedder = None


# === Tools ===

@tool
def search_knowledge_base(query: str) -> str:
    """Useful for answering general questions about stocks, investment strategies, or financial concepts. 
    Use this when the user asks 'What is X?' or 'How does Y work?'."""
    if not client or not embedder:
        return "Knowledge base is currently unavailable."

    try:
        vector = embedder.encode(query)
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector.tolist(),
            limit=TOP_K
        )
        contexts = []
        for result in results:
            payload = result.payload
            if "question" in payload and "answer" in payload:
                contexts.append(f"Q: {payload['question']}\nA: {payload['answer']}")
            elif "text" in payload:
                contexts.append(payload['text'])
        
        if not contexts:
            return "No relevant information found in the knowledge base."
            
        return "\n\n".join(contexts)
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"

@tool
def get_user_details() -> str:
    """Gets the current user's details, including username, email, and balance."""
    try:
        user_id = user_model.load_user_id()
        if not user_id:
            return "Error: Could not identify current user."
        
        user_resp = requests.get(f"{API_URL}/users/{user_id}")
        if user_resp.status_code != 200:
            return "Error: Could not fetch user details."
            
        data = user_resp.json()
        return f"User: {data.get('Username')}, Email: {data.get('Email')}, Balance: ${data.get('Balance')}"
    except Exception as e:
        return f"Error fetching user details: {str(e)}"

@tool
def buy_stock(symbol: str, quantity: int) -> str:
    """Buys a specified quantity of a stock. 
    Args:
        symbol: The stock ticker symbol (e.g., AAPL).
        quantity: The number of shares to buy.
    """
    try:
        user_id = user_model.load_user_id()
        if not user_id:
            return "Error: Could not identify current user."

        # Get current price
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1d")
        if history.empty:
            return f"Error: Could not fetch price for {symbol}."
        
        current_price = history["Close"].iloc[-1]
        total_cost = current_price * quantity

        # Check balance
        user_resp = requests.get(f"{API_URL}/users/{user_id}")
        if user_resp.status_code != 200:
            return "Error: Could not fetch user balance."
        
        balance = float(user_resp.json().get("Balance", 0.0))
        
        if balance < total_cost:
            return f"Insufficient funds. You have ${balance:.2f}, but need ${total_cost:.2f}."

        # Execute Transaction
        transaction_data = {
            "UserID": user_id,
            "StockSymbol": symbol.upper(),
            "Quantity": quantity,
            "PricePerStock": round(current_price, 2)
        }
        
        resp = requests.post(f"{API_URL}/transactions", json=transaction_data)
        if resp.status_code == 201:
            return f"Successfully bought {quantity} shares of {symbol} at ${current_price:.2f}. Total: ${total_cost:.2f}."
        else:
            return f"Transaction failed: {resp.text}"

    except Exception as e:
        return f"Error executing buy: {str(e)}"

@tool
def sell_stock(symbol: str, quantity: int) -> str:
    """Sells a specified quantity of a stock.
    Args:
        symbol: The stock ticker symbol (e.g., AAPL).
        quantity: The number of shares to sell (must be positive).
    """
    try:
        user_id = user_model.load_user_id()
        if not user_id:
            return "Error: Could not identify current user."

        # Get current price
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1d")
        if history.empty:
            return f"Error: Could not fetch price for {symbol}."
        current_price = history["Close"].iloc[-1]

        # Check ownership
        resp = requests.get(f"{API_URL}/users/{user_id}/transactions")
        if resp.status_code != 200:
            return "Error: Could not fetch portfolio."
        
        transactions = resp.json()
        owned_qty = sum(t.get("Quantity", 0) for t in transactions if t.get("StockSymbol") == symbol.upper())
        
        if owned_qty < quantity:
            return f"Insufficient shares. You own {owned_qty} shares of {symbol}."

        # Execute Transaction (Negative quantity for sell)
        transaction_data = {
            "UserID": user_id,
            "StockSymbol": symbol.upper(),
            "Quantity": -1 * quantity, 
            "PricePerStock": round(current_price, 2)
        }
        
        resp = requests.post(f"{API_URL}/transactions", json=transaction_data)
        if resp.status_code == 201:
            total_value = current_price * quantity
            return f"Successfully sold {quantity} shares of {symbol} at ${current_price:.2f}. Total value: ${total_value:.2f}."
        else:
            return f"Transaction failed: {resp.text}"

    except Exception as e:
        return f"Error executing sell: {str(e)}"

@tool
def get_stock_price(symbol: str) -> str:
    """Gets the current price of a stock."""
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1d")
        if history.empty:
            return f"Could not find price for {symbol}."
        price = history["Close"].iloc[-1]
        return f"The current price of {symbol.upper()} is ${price:.2f}."
    except Exception as e:
        return f"Error fetching price: {str(e)}"

@tool
def get_user_portfolio() -> str:
    """Gets the current user's portfolio holdings (stocks owned) and their current market value."""
    try:
        user_id = user_model.load_user_id()
        if not user_id:
            return "Error: Could not identify current user."
        
        # 1. Fetch all transactions
        resp = requests.get(f"{API_URL}/users/{user_id}/transactions")
        if resp.status_code != 200:
            return "Error: Could not fetch transactions to calculate portfolio."
            
        transactions = resp.json()
        
        # 2. Aggregate quantity per stock
        holdings = {}
        for t in transactions:
            symbol = t['StockSymbol'].upper()
            qty = t['Quantity']
            holdings[symbol] = holdings.get(symbol, 0) + qty
            
        # Filter out zero or negative holdings (if any)
        # Assuming we only care about what they currently HOLD > 0
        current_holdings = {k: v for k, v in holdings.items() if v > 0}
        
        if not current_holdings:
            return "You currently have no stocks in your portfolio."

        # 3. Fetch current prices and calculate value
        summary_lines = []
        total_portfolio_value = 0.0
        
        for symbol, qty in current_holdings.items():
            try:
                ticker = yf.Ticker(symbol)
                # fast fetch
                price = 0.0
                history = ticker.history(period="1d")
                if not history.empty:
                    price = history["Close"].iloc[-1]
                
                value = price * qty
                total_portfolio_value += value
                summary_lines.append(f"- {symbol}: {qty} shares @ ${price:.2f} = ${value:.2f}")
            except Exception as e:
                summary_lines.append(f"- {symbol}: {qty} shares (Error fetching price)")

        summary = "Current Portfolio:\n" + "\n".join(summary_lines)
        summary += f"\n\nTotal Portfolio Value: ${total_portfolio_value:.2f}"
        
        return summary

    except Exception as e:
        return f"Error calculating portfolio: {str(e)}"

# === Agent Setup ===

# Tools list
tools = [search_knowledge_base, buy_stock, sell_stock, get_stock_price, get_user_details, get_user_portfolio]

# Initialize LLM with tools
llm = ChatOllama(model=MODEL_NAME, temperature=0).bind_tools(tools)

# System Prompt
system_prompt = """You are a stock trading assistant. 
You can buy/sell stocks, check stock prices, check user details (balance), check portfolio holdings, and answer questions using your knowledge base.

Rules:
1. ONLY use the tools provided. Do not hallucinate other tools.
2. If you need to check the user's balance, use 'get_user_details'.
3. If the user asks about their stocks/holdings/portfolio, use 'get_user_portfolio'.
4. After buying/selling, you can confirm the action. 
5. If the user asks a question you don't know, use 'search_knowledge_base'.
"""

# Creating graph agent (ReAct style) using langgraph prebuilt
# passing system prompt via 'prompt' argument (messages list) to seed the conversation
agent_graph = create_react_agent(llm, tools, prompt=system_prompt)

def get_chat_response(user_input: str) -> str:
    """
    Main entry point for the chat interface.
    """
    try:
        # LangGraph invoke takes {"messages": [...]}
        inputs = {"messages": [HumanMessage(content=user_input)]}
        response = agent_graph.invoke(inputs)
        
        # The result 'response' is the final state. 
        # 'messages' key contains the full conversation history. 
        # The last message is the AI's final response.
        return response["messages"][-1].content
    except Exception as e:
        return f"Error processing request: {str(e)}"


if __name__ == "__main__":
    print("Agent initialized. Type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        
        print("\nAgent processing...")
        answer = get_chat_response(user_input)
        print(f"Agent: {answer}")
