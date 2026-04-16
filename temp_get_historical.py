import yfinance as yf
import pandas as pd
from typing import Optional
import streamlit as st

@st.cache_data(ttl=3600, show_spinner=False)
def get_historical_data(symbol: str, resolution: str = 'D', count: int = 260) -> Optional[pd.DataFrame]:
    """
    Get historical candlestick data using yfinance (Finnhub Free Tier blocks /stock/candle).
    """
    try:
        symbol = symbol.strip().upper()
        # Convert daily count to rough period equivalent for yfinance. 260 trading days ~ 1 year
        period = '1y'
        if count <= 5: period = '5d'
        elif count <= 21: period = '1mo'
        elif count <= 63: period = '3mo'
        elif count <= 126: period = '6mo'
        elif count <= 504: period = '2y'
        elif count <= 1260: period = '5y'
        
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        
        if df.empty:
            return pd.DataFrame()
            
        # Standardize expected columns
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
        df.index.name = 'Date'
        # ensure timezone naive index for compatibility
        if df.index.tz is not None:
            df.index = df.index.tz_convert(None)
            
        # trim to requested count
        df = df.tail(count)
        return df
    except Exception as e:
        return pd.DataFrame()
