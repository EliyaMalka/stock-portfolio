import uvicorn
import webbrowser
import threading
import time
import sys
import os

def open_browser():
    print("Opening browser at http://127.0.0.1:8000/docs ...")
    time.sleep(2) # Wait for server to start
    webbrowser.open("http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    # Start the browser in a separate thread so it doesn't block the server
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the server
    # We use "app.main:app" string for reload=True to work
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
