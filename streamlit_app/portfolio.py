"""
Portfolio tracking and analysis
Uses Finnhub API for reliable data fetching
"""

import pandas as pd
from finnhub_client import get_quote, get_historical_data
from typing import Dict, List
import time


def get_stock_performance(symbol: str, days: int = 30) -> Dict:
    """Get stock performance over N days"""
    try:
        time.sleep(1.1)  # Rate limiting

        # Get current price
        quote = get_quote(symbol)
        if not quote:
            return None

        current_price = quote.get('c')
        if not current_price:
            return None

        # Get historical data
        hist = get_historical_data(symbol)

        if hist.empty or len(hist) < 2:
            return None

        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]

        change = end_price - start_price
        change_pct = (change / start_price * 100) if start_price > 0 else 0
        high = hist['Close'].max()
        low = hist['Close'].min()

        return {
            'symbol': symbol,
            'current_price': current_price,
            'start_price': start_price,
            'end_price': end_price,
            'change': change,
            'change_pct': change_pct,
            'high': high,
            'low': low,
            'period_days': days,
            'company_name': symbol
        }
    except Exception as e:
        return None


def get_portfolio_summary(watchlist: List[str], period_days: int = 30) -> pd.DataFrame:
    """Get summary of all stocks in watchlist"""
    data = []

    for symbol in watchlist:
        perf = get_stock_performance(symbol, period_days)
        if perf:
            data.append({
                'Stock': symbol,
                'Company': perf['company_name'],
                'Price': f"${perf['current_price']:.2f}",
                'Change': f"{perf['change_pct']:+.2f}%",
                'High': f"${perf['high']:.2f}",
                'Low': f"${perf['low']:.2f}",
                'Change_Raw': perf['change_pct']  # For sorting
            })
        time.sleep(0.3)  # Avoid rate limiting

    if data:
        df = pd.DataFrame(data)
        df = df.sort_values('Change_Raw', ascending=False)
        return df[['Stock', 'Company', 'Price', 'Change', 'High', 'Low']]

    return pd.DataFrame()


def calculate_portfolio_gains_if_invested(watchlist: List[str], invested_per_stock: float = 1000) -> Dict:
    """Calculate hypothetical gains if invested equally in all watchlist stocks"""
    total_invested = invested_per_stock * len(watchlist)
    total_current = 0
    gains = []

    for symbol in watchlist:
        perf = get_stock_performance(symbol, 30)
        if perf:
            shares = invested_per_stock / perf['start_price']
            current_value = shares * perf['current_price']
            gain = current_value - invested_per_stock
            gain_pct = (gain / invested_per_stock * 100) if invested_per_stock > 0 else 0

            total_current += current_value
            gains.append({
                'symbol': symbol,
                'invested': invested_per_stock,
                'current_value': current_value,
                'gain': gain,
                'gain_pct': gain_pct
            })
        time.sleep(0.3)

    total_gain = total_current - total_invested
    total_gain_pct = (total_gain / total_invested * 100) if total_invested > 0 else 0

    return {
        'total_invested': total_invested,
        'total_current': total_current,
        'total_gain': total_gain,
        'total_gain_pct': total_gain_pct,
        'stocks': gains
    }
