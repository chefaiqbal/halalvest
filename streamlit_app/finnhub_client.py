"""
Finnhub API Client
Provides reliable stock data fetching from Finnhub (60 calls/min free tier)
"""

import requests
import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import time
import os
import streamlit as st
import logging
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get API key from environment or Streamlit secrets
try:
    FINNHUB_API_KEY = st.secrets.get("FINNHUB_API_KEY", os.getenv("FINNHUB_API_KEY", ""))
except Exception as e:
    FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")

logger.info(f"🔑 API Key loaded: {bool(FINNHUB_API_KEY)}")
if FINNHUB_API_KEY:
    logger.info(f"✅ API Key length: {len(FINNHUB_API_KEY)} characters")
    logger.info(f"📌 API Key preview: {FINNHUB_API_KEY[:10]}...")
else:
    logger.error("❌ ERROR: FINNHUB_API_KEY is not set!")
    print("❌ ERROR: FINNHUB_API_KEY is not configured in Streamlit Secrets")

FINNHUB_BASE_URL = "https://finnhub.io/api/v1"
REQUEST_DELAY = 1.1  # 1.1 seconds between requests to stay under 60/min limit


def _make_request(endpoint: str, params: Dict = None, max_retries: int = 3) -> Optional[Dict]:
    """
    Make a request to Finnhub API with retry logic and rate limiting
    """
    if not FINNHUB_API_KEY:
        logger.error("❌ No API key available for request")
        return None

    url = f"{FINNHUB_BASE_URL}{endpoint}"
    if params is None:
        params = {}
        
    if 'symbol' in params and isinstance(params['symbol'], str):
        params['symbol'] = params['symbol'].strip().upper()
        
    params['token'] = FINNHUB_API_KEY

    logger.info(f"📡 Making request to: {endpoint}")
    retry_delay = 2
    for attempt in range(max_retries):
        try:
            time.sleep(REQUEST_DELAY)  # Rate limiting
            response = requests.get(url, params=params, timeout=10)
            logger.info(f"📊 Response status: {response.status_code}")
            response.raise_for_status()
            data = response.json()

            # Check for rate limit response
            if isinstance(data, dict) and data.get('error'):
                logger.error(f"⚠️ API Error: {data.get('error')}")
                if 'rate' in data.get('error', '').lower():
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                return None

            logger.info(f"✅ Data received successfully from {endpoint}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request error on attempt {attempt + 1}/{max_retries}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                return None

    return None


@st.cache_data(ttl=3600, show_spinner=False)
def get_quote(symbol: str) -> Optional[Dict]:
    """Get real-time stock quote"""
    return _make_request("/quote", {"symbol": symbol})


@st.cache_data(ttl=3600, show_spinner=False)
def get_company_profile(symbol: str) -> Optional[Dict]:
    """Get company profile (sector, industry, name, etc.)"""
    return _make_request("/stock/profile2", {"symbol": symbol})


@st.cache_data(ttl=3600, show_spinner=False)
def get_fundamental_ratios(symbol: str) -> Optional[Dict]:
    """Get fundamental ratios (P/E, ROE, etc.)"""
    return _make_request("/stock/metric", {
        "symbol": symbol,
        "metric": "all"
    })


@st.cache_data(ttl=3600, show_spinner=False)
@st.cache_data(ttl=3600, show_spinner=False)
def get_historical_data(symbol: str, resolution: str = 'D', count: int = 260) -> Optional[pd.DataFrame]:
    """
    Get historical candlestick data using yfinance (Finnhub Free blocks /stock/candle).
    Includes multiple retry mechanisms if Yahoo Finance rate limits it.
    """
    symbol = symbol.strip().upper()
    period = '1y'
    if count <= 5: period = '5d'
    elif count <= 21: period = '1mo'
    elif count <= 63: period = '3mo'
    elif count <= 126: period = '6mo'
    elif count <= 504: period = '2y'
    elif count <= 1260: period = '5y'
    
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, auto_adjust=True, back_adjust=False)
            
            if df.empty:
                return pd.DataFrame()
                
            # Standardize expected columns
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
            df.index.name = 'Date'
            if df.index.tz is not None:
                df.index = df.index.tz_convert(None)
                
            df = df.tail(count)
            return df
            
        except Exception as e:
            err_msg = str(e).lower()
            if "too many requests" in err_msg or "rate limit" in err_msg:
                logger.warning(f"⚠️ Yahoo Finance Rate Limit on attempt {attempt+1}/{max_retries}. Sleeping for {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                logger.error(f"Error fetching historical data: {e}")
                return pd.DataFrame()
                
    logger.error("❌ Exhausted retries for Yahoo Finance historical data.")
    return pd.DataFrame()


def get_company_news(symbol: str, limit: int = 5) -> List[Dict]:
    """Get latest company news"""
    try:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        data = _make_request("/company-news", {
            "symbol": symbol,
            "from": start_date,
            "to": end_date
        })
        if data and isinstance(data, list):
            return data[:limit]
        return []
    except Exception as e:
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
    except Exception as e:
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
    except Exception as e:
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
    except Exception as e:
        return {'trend': 'N/A', 'avg_volume': 0, 'current_volume': 0, 'ratio': 1}
