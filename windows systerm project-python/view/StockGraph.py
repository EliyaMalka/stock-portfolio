"""
Stock Graph View Component.

Responsible for rendering the interactive stock price chart using Matplotlib
embedded within a PySide6 widget. Allows users to select a stock symbol
and a time period (daily, weekly, yearly) to fetch and display historical data from Yahoo Finance.
"""
import sys
import pandas as pd
import os
import yfinance as yf
import matplotlib.subplots as subplots
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                               QComboBox, QRadioButton, QHBoxLayout, QLabel)
from PySide6.QtCore import QTimer,QFile, QTextStream
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates

class StockGraph(QWidget):
    """
    Widget containing the stock selection controls and the Matplotlib canvas.
    """
    def __init__(self):
        """Initializes the UI, default selections, timezone cache workaround, and starts the auto-refresh timer."""
        super().__init__()
        self.symbol = "NVDA"
        self.period = "1y"

        # --- Fix for timezone cache (critical for Windows users with non-ASCII names) ---
        cache_dir = os.path.join(os.getcwd(), "py_cache")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        try:
            yf.set_tz_cache_location(cache_dir)
        except:
            pass

        
        self.initUI()
        self.update_graph()

    def initUI(self):
        """Builds the layouts, combo boxes, radio buttons, and the Matplotlib canvas."""
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_layout.setSpacing(20)  # ריווח בין שתי הקבוצות (Stock ו-Period)

        # --- Stock Selection ---
        stock_container = QWidget()
        stock_layout = QHBoxLayout()
        stock_layout.setContentsMargins(0, 0, 0, 0)
        stock_layout.setSpacing(6) 
        stock_container.setLayout(stock_layout)

        stock_label = QLabel("Stock:")
        stock_label.setObjectName("inlineLabel")

        self.stock_selector = QComboBox()
        self.stock_selector.addItems(["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "TSMC", "ARM", "SSNLF", "NVDA", "ASML", "META"])
        self.stock_selector.setCurrentText("NVDA")
        self.stock_selector.currentTextChanged.connect(self.update_symbol)

        stock_layout.addWidget(stock_label)
        stock_layout.addWidget(self.stock_selector)

        # --- Period Selection ---
        period_container = QWidget()
        period_layout = QHBoxLayout()
        period_layout.setContentsMargins(0, 0, 0, 0)
        period_layout.setSpacing(6)
        period_container.setLayout(period_layout)

        period_label = QLabel("Period:")
        period_label.setObjectName("inlineLabel")

        self.daily_radio = QRadioButton("Daily")
        self.weekly_radio = QRadioButton("Weekly")
        self.yearly_radio = QRadioButton("Yearly")
        self.yearly_radio.setChecked(True)

        self.daily_radio.toggled.connect(lambda: self.update_period("1d"))
        self.weekly_radio.toggled.connect(lambda: self.update_period("1wk"))
        self.yearly_radio.toggled.connect(lambda: self.update_period("1y"))

        period_layout.addWidget(period_label)
        period_layout.addWidget(self.daily_radio)
        period_layout.addWidget(self.weekly_radio)
        period_layout.addWidget(self.yearly_radio)

        # Add both groups to top_layout
        top_layout.addWidget(stock_container)
        top_layout.addWidget(period_container)
        top_layout.addStretch(1)

        # Matplotlib Graph Setup
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        layout.addLayout(top_layout)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.load_stylesheet(r"view\stockGraph.qss")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(300000) # Auto-refresh every 5 minutes


    def load_stylesheet(self, path):
        """Loads and applies the QSS styling for the widget."""
        file = QFile(path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close()
            
    def update_symbol(self, text):
        """Slot to handle stock symbol change and trigger a graph update."""
        self.symbol = text
        self.update_graph()

    def update_period(self, period):
        """Slot to handle time period change and trigger a graph update."""
        self.period = period
        self.update_graph()

    def fetch_stock_data(self):
        """Fetches historical stock data from Yahoo Finance based on current selections."""
        try:
            print(f"Fetching data for {self.symbol} ({self.period})...")
            interval = "1d" if self.period == "1y" else "1h"
            # auto_adjust=True helps get the actual price often expected
            data = yf.download(self.symbol, period=self.period, interval=interval, progress=False, auto_adjust=False)
            
            if data.empty:
                print(f"Warning: No data returned for {self.symbol}")
                return None
            else:
                print(f"Data fetched successfully. Rows: {len(data)}")
                return data

        except Exception as e:
            print(f"Error fetching stock data for {self.symbol}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def update_graph(self):
        """Fetches new data, clears the old plot, and renders the new plot with proper formatting."""
        data = self.fetch_stock_data()
        if data is not None and not data.empty:
            self.ax.clear()
            try:
                # Robustly extract the 'Close' column handling MultiIndex
                y_values = None
                
                # Check if columns are MultiIndex (common in new yfinance)
                if isinstance(data.columns, pd.MultiIndex):
                    try:
                        # Try to access using the symbol if it exists in the columns level
                        y_values = data["Close"][self.symbol]
                    except KeyError:
                        # Fallback: maybe it's just 'Close' or the structure is different
                        if "Close" in data.columns:
                             y_values = data["Close"]
                else:
                    # Flat Index
                    if "Close" in data.columns:
                        y_values = data["Close"]

                if y_values is None:
                    print(f"Error: Could not extract 'Close' prices. Columns: {data.columns}")
                    self.ax.text(0.5, 0.5, "Error: Data format mismatch", ha='center', va='center')
                    return

                self.ax.plot(data.index, y_values, color="green", label=self.symbol)
            except Exception as e:
                print(f"Error plotting graph: {e}")
                self.ax.text(0.5, 0.5, f"Error plotting: {e}", ha='center', va='center')
                return

            self.ax.set_title(f"Stock Price: {self.symbol} ({self.period})", fontsize=14, fontweight='bold')
            self.ax.set_xlabel("Date", fontsize=12)
            self.ax.set_ylabel("Price (USD)", fontsize=12)
            self.ax.legend()
            
            if self.period == "1d":
                self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            elif self.period == "1wk":
                self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%a'))
            else:
                self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.canvas.draw()

