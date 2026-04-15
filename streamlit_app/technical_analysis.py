"""
Technical Analysis Service
Implements technical indicators: SMA, RSI, MACD, Volume trends
Uses Finnhub API for reliable data fetching
"""

import pandas as pd
import numpy as np
from finnhub_client import (
    get_historical_data as fetch_historical_data,
    calculate_sma as calc_sma,
    calculate_rsi as calc_rsi,
    calculate_macd as calc_macd,
    calculate_volume_trend as calc_volume_trend
)
from typing import Dict, Tuple


def get_historical_data(symbol: str, period: str = '1y') -> pd.DataFrame:
    """Fetch historical stock data from Finnhub"""
    df = fetch_historical_data(symbol)
    return df if df is not None else pd.DataFrame()


def calculate_sma(df: pd.DataFrame, columns: list = [20, 50, 200]) -> Dict:
    """Calculate Simple Moving Averages"""
    return calc_sma(df, columns)


def calculate_rsi(df: pd.DataFrame, period: int = 14) -> float:
    """Calculate Relative Strength Index"""
    return calc_rsi(df, period)


def calculate_macd(df: pd.DataFrame) -> Dict:
    """Calculate MACD (Moving Average Convergence Divergence)"""
    return calc_macd(df)


def calculate_volume_trend(df: pd.DataFrame, period: int = 20) -> Dict:
    """Analyze volume trends"""
    return calc_volume_trend(df, period)


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
