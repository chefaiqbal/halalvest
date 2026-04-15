"""
Finnhub API Client
Provides reliable stock data fetching from Finnhub (60 calls/min free tier)
"""

import requests
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import time
import os
import streamlit as st

# Get API key from environment or Streamlit secrets
try:
    FINNHUB_API_KEY = st.secrets.get("FINNHUB_API_KEY", os.getenv("FINNHUB_API_KEY", ""))
except:
    FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")

FINNHUB_BASE_URL = "https://finnhub.io/api/v1"
REQUEST_DELAY = 1.1  # 1.1 seconds between requests to stay under 60/min limit


def _make_request(endpoint: str, params: Dict = None, max_retries: int = 3) -> Optional[Dict]:
    """
    Make a request to Finnhub API with retry logic and rate limiting
    """
    if not FINNHUB_API_KEY:
        return None

    url = f"{FINNHUB_BASE_URL}{endpoint}"
    if params is None:
        params = {}
    params['token'] = FINNHUB_API_KEY

    retry_delay = 2
    for attempt in range(max_retries):
        try:
            time.sleep(REQUEST_DELAY)  # Rate limiting
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Check for rate limit response
            if isinstance(data, dict) and data.get('error'):
                if 'rate' in data.get('error', '').lower():
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                return None

            return data
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                return None

    return None


def get_quote(symbol: str) -> Optional[Dict]:
    """Get real-time stock quote"""
    return _make_request("/quote", {"symbol": symbol})


def get_company_profile(symbol: str) -> Optional[Dict]:
    """Get company profile (sector, industry, name, etc.)"""
    return _make_request("/stock/profile2", {"symbol": symbol})


def get_fundamental_ratios(symbol: str) -> Optional[Dict]:
    """Get fundamental ratios (P/E, ROE, etc.)"""
    return _make_request("/stock/metric", {
        "symbol": symbol,
        "metric": "all"
    })


def get_historical_data(symbol: str, resolution: str = 'D', count: int = 260) -> Optional[pd.DataFrame]:
    """
    Get historical candlestick data
    resolution: D=daily, W=weekly, M=monthly
    count: number of candles (260 = ~1 year of trading days)
    """
    try:
        # Get current timestamp
        to_timestamp = int(time.time())
        # Calculate from_timestamp (approximately 1 year ago)
        from_timestamp = to_timestamp - (count * 86400)  # Approximate

        data = _make_request("/stock/candle", {
            "symbol": symbol,
            "resolution": resolution,
            "from": from_timestamp,
            "to": to_timestamp
        })

        if not data or data.get('s') == 'no_data':
            return pd.DataFrame()

        # Convert Finnhub format to DataFrame
        df = pd.DataFrame({
            'Date': pd.to_datetime(data.get('t', []), unit='s'),
            'Open': data.get('o', []),
            'High': data.get('h', []),
            'Low': data.get('l', []),
            'Close': data.get('c', []),
            'Volume': data.get('v', [])
        })

        if df.empty:
            return df

        df.set_index('Date', inplace=True)
        return df.sort_index()

    except Exception as e:
        return pd.DataFrame()


def get_company_news(symbol: str, limit: int = 5) -> List[Dict]:
    """Get latest company news"""
    try:
        data = _make_request("/company-news", {
            "symbol": symbol,
            "limit": limit
        })
        return data if data else []
    except:
        return []


def calculate_sma(df: pd.DataFrame, columns: List[int] = None) -> Dict[int, float]:
    """Calculate Simple Moving Averages"""
    if columns is None:
        columns = [20, 50, 200]

    sma_dict = {}
    for period in columns:
        if len(df) >= period:
            df[f'SMA_{period}'] = df['Close'].rolling(window=period).mean()
            sma_dict[period] = df[f'SMA_{period}'].iloc[-1]

    return sma_dict


def calculate_rsi(df: pd.DataFrame, period: int = 14) -> Optional[float]:
    """Calculate Relative Strength Index"""
    if len(df) < period:
        return None

    try:
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]
    except:
        return None


def calculate_macd(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate MACD (Moving Average Convergence Divergence)"""
    try:
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()

        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal

        return {
            'macd': macd.iloc[-1],
            'signal': signal.iloc[-1],
            'histogram': histogram.iloc[-1],
        }
    except:
        return {'macd': 0, 'signal': 0, 'histogram': 0}


def calculate_volume_trend(df: pd.DataFrame, period: int = 20) -> Dict:
    """Analyze volume trends"""
    if len(df) < period:
        return {'trend': 'N/A', 'avg_volume': 0, 'current_volume': 0, 'ratio': 1}

    try:
        current_volume = df['Volume'].iloc[-1]
        avg_volume = df['Volume'].tail(period).mean()
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1

        if volume_ratio > 1.3:
            trend = 'High (Bullish signal)'
        elif volume_ratio > 1.0:
            trend = 'Above Average'
        elif volume_ratio < 0.7:
            trend = 'Low (Potential weakness)'
        else:
            trend = 'Average'

        return {
            'trend': trend,
            'current_volume': current_volume,
            'avg_volume': avg_volume,
            'ratio': volume_ratio
        }
    except:
        return {'trend': 'N/A', 'avg_volume': 0, 'current_volume': 0, 'ratio': 1}
