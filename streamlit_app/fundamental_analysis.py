"""
Fundamental Analysis Service
Analyzes P/E ratios, debt-to-equity, ROE, profit margins
"""

import yfinance as yf
from typing import Dict, Tuple
import time


def get_fundamental_metrics(symbol: str) -> Dict:
    """Fetch fundamental metrics for a stock"""
    try:
        time.sleep(0.2)  # Add delay to avoid rate limiting
        ticker = yf.Ticker(symbol)
        info = ticker.info

        return {
            'pe_ratio': info.get('trailingPE'),
            'forward_pe': info.get('forwardPE'),
            'peg_ratio': info.get('pegRatio'),
            'debt_to_equity': info.get('debtToEquity'),
            'current_ratio': info.get('currentRatio'),
            'quick_ratio': info.get('quickRatio'),
            'roe': info.get('returnOnEquity'),  # ROE - Return on Equity
            'roa': info.get('returnOnAssets'),  # ROA - Return on Assets
            'profit_margin': info.get('profitMargins'),  # Net profit margin
            'operating_margin': info.get('operatingMargins'),
            'gross_margin': info.get('grossMargins'),
            'earnings_growth': info.get('earningsGrowth'),
            'revenue_growth': info.get('revenueGrowth'),
            'dividend_yield': info.get('dividendYield'),
            'market_cap': info.get('marketCap'),
            'enterprise_value': info.get('enterpriseValue'),
            'free_cash_flow': info.get('freeCashflow'),
            'book_value': info.get('bookValue'),
            'forward_earnings': info.get('forwardEps'),
            'trailing_earnings': info.get('trailingEps'),
        }
    except Exception as e:
        return {}


def evaluate_pe_ratio(pe: float, industry_avg: float = 20) -> Tuple[str, float]:
    """
    Evaluate P/E ratio
    Returns: (interpretation, score)
    """
    if pe is None:
        return "N/A", 50

    if pe < 0:
        return "❌ Negative earnings", 20
    elif pe < 15:
        return "✅ Undervalued", 80
    elif pe < industry_avg:
        return "✅ Below industry average", 75
    elif pe < industry_avg * 1.2:
        return "〰️ Near industry average", 60
    elif pe < 30:
        return "⚠️ Premium valuation", 45
    else:
        return "❌ Very expensive", 25


def evaluate_debt_to_equity(de: float) -> Tuple[str, float]:
    """
    Evaluate debt-to-equity ratio (Islamic finance consideration)
    Returns: (interpretation, score)
    """
    if de is None:
        return "N/A", 50

    if de < 0.5:
        return "✅ Very healthy", 90
    elif de < 1.0:
        return "✅ Good financial health", 80
    elif de < 1.5:
        return "⚠️ Acceptable leverage", 60
    elif de < 2.0:
        return "⚠️ Elevated leverage", 40
    else:
        return "❌ High risk", 20


def evaluate_roe(roe: float) -> Tuple[str, float]:
    """
    Evaluate Return on Equity (profitability efficiency)
    Returns: (interpretation, score)
    """
    if roe is None:
        return "N/A", 50

    if roe < 0.05:
        return "❌ Poor", 20
    elif roe < 0.10:
        return "⚠️ Below average", 40
    elif roe < 0.15:
        return "✅ Good", 70
    elif roe < 0.20:
        return "✅ Very good", 85
    else:
        return "✅ Excellent", 95


def evaluate_profit_margin(margin: float) -> Tuple[str, float]:
    """
    Evaluate net profit margin (operational efficiency)
    Returns: (interpretation, score)
    """
    if margin is None:
        return "N/A", 50

    if margin < 0.02:
        return "❌ Very low", 20
    elif margin < 0.05:
        return "⚠️ Low", 40
    elif margin < 0.10:
        return "✅ Good", 70
    elif margin < 0.20:
        return "✅ Excellent", 85
    else:
        return "✅ Outstanding", 95


def fundamental_analysis(symbol: str) -> Dict:
    """Comprehensive fundamental analysis"""
    metrics = get_fundamental_metrics(symbol)

    # Evaluate individual metrics
    pe_interp, pe_score = evaluate_pe_ratio(metrics.get('pe_ratio'))
    de_interp, de_score = evaluate_debt_to_equity(metrics.get('debt_to_equity'))
    roe_interp, roe_score = evaluate_roe(metrics.get('roe'))
    pm_interp, pm_score = evaluate_profit_margin(metrics.get('profit_margin'))

    # Calculate average fundamental score
    scores = [s for s in [pe_score, de_score, roe_score, pm_score] if s > 0]
    fundamental_score = sum(scores) / len(scores) if scores else 50

    return {
        'metrics': metrics,
        'pe_ratio': metrics.get('pe_ratio'),
        'pe_interpretation': pe_interp,
        'pe_score': pe_score,
        'debt_to_equity': metrics.get('debt_to_equity'),
        'de_interpretation': de_interp,
        'de_score': de_score,
        'roe': metrics.get('roe'),
        'roe_interpretation': roe_interp,
        'roe_score': roe_score,
        'profit_margin': metrics.get('profit_margin'),
        'pm_interpretation': pm_interp,
        'pm_score': pm_score,
        'fundamental_score': fundamental_score,
        'dividend_yield': metrics.get('dividend_yield'),
        'revenue_growth': metrics.get('revenue_growth'),
    }


def fundamental_signal_score(analysis: Dict) -> Tuple[float, str]:
    """
    Generate fundamental analysis score (0-100)
    Returns: (score, interpretation)
    """
    # Use the average of the metrics
    score = analysis.get('fundamental_score', 50)

    if score > 75:
        interpretation = '📈 Strong Fundamentals'
    elif score > 60:
        interpretation = '✅ Good Fundamentals'
    elif score > 40:
        interpretation = '〰️ Mixed Fundamentals'
    else:
        interpretation = '📉 Weak Fundamentals'

    return score, interpretation

