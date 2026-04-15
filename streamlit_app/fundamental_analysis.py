"""
Fundamental Analysis Service
Analyzes P/E ratios, debt-to-equity, ROE, profit margins
Uses Finnhub API for reliable data fetching
"""

from finnhub_client import get_fundamental_ratios, get_quote, get_company_profile
from typing import Dict, Tuple


def get_fundamental_metrics(symbol: str) -> Dict:
    """Fetch fundamental metrics for a stock from Finnhub"""
    try:
        # Get metrics from Finnhub
        metrics_data = get_fundamental_ratios(symbol)
        quote_data = get_quote(symbol)

        if not metrics_data or not quote_data:
            return {}

        # Extract available metrics
        return {
            'pe_ratio': metrics_data.get('metric', {}).get('peTrailingTTM'),
            'forward_pe': metrics_data.get('metric', {}).get('peForward'),
            'peg_ratio': metrics_data.get('metric', {}).get('pegratio'),
            'debt_to_equity': metrics_data.get('metric', {}).get('debtToEquity'),
            'current_ratio': metrics_data.get('metric', {}).get('currentRatio'),
            'quick_ratio': metrics_data.get('metric', {}).get('quickRatio'),
            'roe': metrics_data.get('metric', {}).get('roe'),
            'roa': metrics_data.get('metric', {}).get('roa'),
            'profit_margin': metrics_data.get('metric', {}).get('grossMargin'),
            'operating_margin': metrics_data.get('metric', {}).get('operatingMarginTTM'),
            'gross_margin': metrics_data.get('metric', {}).get('grossMargin'),
            'earnings_growth': metrics_data.get('metric', {}).get('estimatedEarningsGrowth'),
            'revenue_growth': metrics_data.get('metric', {}).get('revenuePerShare'),
            'dividend_yield': quote_data.get('d'),
            'market_cap': quote_data.get('marketCap'),
            'enterprise_value': metrics_data.get('metric', {}).get('enterpriseToRevenue'),
            'free_cash_flow': metrics_data.get('metric', {}).get('fcfMargin'),
            'book_value': metrics_data.get('metric', {}).get('bookValue'),
            'forward_earnings': quote_data.get('eps'),
            'trailing_earnings': metrics_data.get('metric', {}).get('trailingEpsTTM'),
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
