"""
Technical Analysis Service
Implements technical indicators: SMA, RSI, MACD, Volume trends
"""

import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, Tuple
import time


def get_historical_data(symbol: str, period: str = '1y') -> pd.DataFrame:
    """Fetch historical stock data with retry logic"""
    max_retries = 3
    retry_delay = 3  # Start with 3 seconds

    for attempt in range(max_retries):
        try:
            time.sleep(1)  # Longer delay before each request
            df = yf.download(symbol, period=period, progress=False)
            if len(df) == 0:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                return pd.DataFrame()
            return df
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                return pd.DataFrame()

    return pd.DataFrame()


def calculate_sma(df: pd.DataFrame, columns: list = [20, 50, 200]) -> Dict:
    """Calculate Simple Moving Averages"""
    sma_dict = {}
    for col in columns:
        df[f'SMA_{col}'] = df['Close'].rolling(window=col).mean()
        sma_dict[col] = df[f'SMA_{col}'].iloc[-1]
    return sma_dict


def calculate_rsi(df: pd.DataFrame, period: int = 14) -> float:
    """Calculate Relative Strength Index"""
    if len(df) < period:
        return None

    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]


def calculate_macd(df: pd.DataFrame) -> Dict:
    """Calculate MACD (Moving Average Convergence Divergence)"""
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


def calculate_volume_trend(df: pd.DataFrame, period: int = 20) -> Dict:
    """Analyze volume trends"""
    if len(df) < period:
        return {'trend': 'N/A', 'avg_volume': 0}

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


def technical_analysis(symbol: str) -> Dict:
    """Comprehensive technical analysis"""
    df = get_historical_data(symbol)

    if df.empty:
        return {'error': 'Could not fetch data'}

    sma = calculate_sma(df)
    rsi = calculate_rsi(df)
    macd = calculate_macd(df)
    volume = calculate_volume_trend(df)

    current_price = df['Close'].iloc[-1]
    prev_close = df['Close'].iloc[-2] if len(df) > 1 else current_price

    # Determine trend
    if sma[20] > sma[50] > sma[200]:
        trend = 'Uptrend ⬆️'
    elif sma[20] < sma[50] < sma[200]:
        trend = 'Downtrend ⬇️'
    else:
        trend = 'Sideways 〰️'

    return {
        'current_price': current_price,
        'previous_close': prev_close,
        'price_change': current_price - prev_close,
        'price_change_pct': ((current_price - prev_close) / prev_close * 100) if prev_close > 0 else 0,
        'trend': trend,
        'sma': sma,
        'rsi': rsi,
        'macd': macd,
        'volume': volume,
        'df': df
    }


def technical_signal_score(analysis: Dict) -> Tuple[float, str]:
    """
    Generate technical analysis score (0-100)
    Returns: (score, interpretation)
    """
    score = 50  # Start neutral

    # SMA signals
    sma = analysis.get('sma', {})
    if sma.get(20, 0) > sma.get(50, 0) > sma.get(200, 0):
        score += 20  # Strong uptrend
    elif sma.get(20, 0) < sma.get(50, 0) < sma.get(200, 0):
        score -= 20  # Strong downtrend

    # RSI signals
    rsi = analysis.get('rsi')
    if rsi is not None:
        if rsi < 30:
            score += 15  # Oversold - potential bounce
        elif rsi > 70:
            score -= 15  # Overbought - potential pullback
        elif 40 < rsi < 60:
            score += 5  # Neutral zone

    # MACD signals
    macd = analysis.get('macd', {})
    if macd.get('histogram', 0) > 0 and macd.get('macd', 0) > macd.get('signal', 0):
        score += 10  # Bullish crossover
    elif macd.get('histogram', 0) < 0 and macd.get('macd', 0) < macd.get('signal', 0):
        score -= 10  # Bearish crossover

    # Volume signals
    volume = analysis.get('volume', {})
    if 'High' in volume.get('trend', ''):
        score += 5

    score = max(0, min(100, score))  # Clamp between 0-100

    if score > 65:
        interpretation = '📈 Bullish'
    elif score > 55:
        interpretation = '💹 Moderately Bullish'
    elif score > 45:
        interpretation = '〰️ Neutral'
    elif score > 35:
        interpretation = '💹 Moderately Bearish'
    else:
        interpretation = '📉 Bearish'

    return score, interpretation

