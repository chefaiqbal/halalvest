"""
Halal Stock Screening Service
Screens stocks according to Islamic finance principles
Uses Finnhub API for reliable data fetching
"""

from finnhub_client import get_company_profile, get_fundamental_ratios
from fmp_client import get_halal_metrics_fmp
from typing import List, Dict, Tuple, Optional

# List of prohibited sectors (haram)
PROHIBITED_SECTORS = {
    'alcohol',
    'tobacco',
    'gambling',
    'pork',
    'conventional finance',
    'insurance',
    'weapons',
    'defense',
    'entertainment',  # some controversial content
    'adult entertainment'
}

# Pre-screened S&P 500 halal-compliant stocks (major companies)
HALAL_STOCKS = [
    # Technology
    'NVDA', 'AMD', 'ORCL', 'AVGO', 'ADBE', 'CRM', 'INTU', 'SNPS', 'CDNS', 'NXPI',

    # Healthcare
    'JNJ', 'UNH', 'PFE', 'ABBV', 'MRK', 'TMO', 'LLY', 'AZN', 'AMGN', 'GILD',

    # Industrial
    'BA', 'GE', 'MMM', 'RTX', 'HON', 'LMT', 'NOC', 'GD', 'TXT', 'SPR',

    # Consumer
    'AMZN', 'WMT', 'HD', 'MCD', 'NKE', 'SBUX', 'TJX', 'COST', 'LOW', 'TSCO',

    # Financial Services (select compliant ones)
    'JPM', 'BAC', 'WFC', 'GS', 'MS', 'BLK', 'SCHW', 'CME', 'ICE', 'MSCI',

    # Energy & Materials
    'XOM', 'CVX', 'COP', 'SLB', 'MPC', 'PSX', 'VLO', 'FANG', 'EOG', 'MUR',

    # Communications
    'MSFT', 'GOOG', 'TMUS', 'VZ', 'T', 'CMCSA', 'CHTR',

    # Real Estate (REITs - generally halal if no interest-based)
    'PLD', 'CCI', 'DLR', 'EQIX', 'SPG', 'O', 'VICI', 'STAG', 'STOR', 'PSA',

    # Utilities
    'NEE', 'DUK', 'SO', 'D', 'EXC', 'AEP', 'XEL', 'SRE', 'WEC', 'ES',

    # Industrials
    'CAT', 'DE', 'PACW', 'FDX', 'UPS', 'XRX', 'IRM', 'WM', 'RSG', 'GWW',
]

# Filter to remove some controversial ones
CONTROVERSIAL_IN_HALAL = {'DIS', 'META', 'GOOGL'}  # Entertainment, social media concerns
HALAL_STOCKS = [s for s in HALAL_STOCKS if s not in CONTROVERSIAL_IN_HALAL]


def get_company_info(symbol: str) -> Dict:
    """Get company information for halal screening from Finnhub"""
    try:
        profile = get_company_profile(symbol)
        if not profile:
            return {}

        return {
            'sector': profile.get('finnhubIndustry', 'Unknown'),
            'industry': profile.get('finnhubIndustry', 'Unknown'),
            'company_name': profile.get('name', symbol),
            'market_cap': profile.get('marketCapitalization', 0),
        }
    except Exception as e:
        return {}


def check_debt_to_equity(symbol: str) -> Tuple[float, str]:
    """
    Check debt-to-equity ratio - Islamic finance principle
    Generally, D/E should be < 1.5 for halal compliance
    """
    try:
        metrics_data = get_fundamental_ratios(symbol)
        if not metrics_data:
            return None, 'N/A'

        debt_to_equity = metrics_data.get('metric', {}).get('debtToEquity')

        if debt_to_equity is None:
            return None, 'N/A'

        if debt_to_equity < 0.5:
            return debt_to_equity, '✅ Very Good (Low leverage)'
        elif debt_to_equity < 1.0:
            return debt_to_equity, '✅ Good (Moderate leverage)'
        elif debt_to_equity < 1.5:
            return debt_to_equity, '⚠️ Acceptable (Higher leverage)'
        else:
            return debt_to_equity, '❌ High leverage risk'
    except Exception as e:
        return None, 'N/A'


def evaluate_methodologies(de_ratio: float, sector_compliant: bool, fmp_metrics: Optional[Dict] = None) -> Dict:
    """
    Evaluates the stock against the major Islamic Finance Methodologies.
    Uses precise Balance Sheet data from FMP if available, falling back to Finnhub proxies.
    """
    if fmp_metrics and fmp_metrics.get("total_assets", 0) > 0:
        market_cap = fmp_metrics.get("market_cap", 0)
        total_debt = fmp_metrics.get("total_debt", 0)
        total_assets = fmp_metrics.get("total_assets", 0)
        
        # Calculate precise balance sheet metrics
        debt_to_mc = (total_debt / market_cap) if market_cap > 0 else float('inf')
        debt_to_assets = (total_debt / total_assets) if total_assets > 0 else float('inf')
        
        return {
            "AAOIFI (Accurate)": {
                "pass": sector_compliant and debt_to_mc < 0.30,
                "rule": f"Debt / Market Cap < 30% (Actual: {debt_to_mc*100:.1f}%)",
                "status_text": "✅ Pass" if (sector_compliant and debt_to_mc < 0.30) else "❌ Fail"
            },
            "S&P Shariah (Proxy)": {
                "pass": sector_compliant and debt_to_mc < 0.33,
                "rule": f"Debt / Curr. Market Cap < 33% (Actual: {debt_to_mc*100:.1f}%)",
                "status_text": "✅ Pass" if (sector_compliant and debt_to_mc < 0.33) else "❌ Fail"
            },
            "FTSE Shariah (Accurate)": {
                "pass": sector_compliant and debt_to_assets < 0.333,
                "rule": f"Debt / Total Assets < 33.3% (Actual: {debt_to_assets*100:.1f}%)",
                "status_text": "✅ Pass" if (sector_compliant and debt_to_assets < 0.333) else "❌ Fail"
            }
        }

    # STANDARD PROXIES (If FMP API is not configured)
    if de_ratio is None:
        return {}

    # AAOIFI: Debt / Market Cap < 30% (Proxy: D/E < 0.43 to imply D/A < 30%)
    # S&P Shariah: Debt / Market Cap < 33% (Proxy: D/E < 0.49 to imply D/A < 33%)
    # FTSE Shariah: Debt / Total Assets < 33.3% (Proxy: D/E < 0.50 to equal D/A < 33.3%)
    
    return {
        "AAOIFI (Proxy)": {
            "pass": sector_compliant and de_ratio < 0.43,
            "rule": "Debt / Market Cap < 30%",
            "status_text": "✅ Pass" if (sector_compliant and de_ratio < 0.43) else "❌ Fail"
        },
        "S&P Shariah (Proxy)": {
            "pass": sector_compliant and de_ratio < 0.49,
            "rule": "Debt / 36mo avg Market Cap < 33%",
            "status_text": "✅ Pass" if (sector_compliant and de_ratio < 0.49) else "❌ Fail"
        },
        "FTSE Shariah (Proxy)": {
            "pass": sector_compliant and de_ratio < 0.50,
            "rule": "Debt / Total Assets < 33.3%",
            "status_text": "✅ Pass" if (sector_compliant and de_ratio < 0.50) else "❌ Fail"
        }
    }


def screen_stock_halal(symbol: str) -> Dict:
    """
    Screen a stock for halal compliance
    Returns: {is_halal, compliance_score, issues, details}
    """
    info = get_company_info(symbol)
    sector = info.get('sector', '').lower()
    industry = info.get('industry', '').lower()

    issues = []
    compliance_scores = []

    # Check sector
    sector_compliant = True
    for prohibited in PROHIBITED_SECTORS:
        if prohibited in sector or prohibited in industry:
            issues.append(f"Prohibited sector: {sector}/{industry}")
            sector_compliant = False
            break

    if sector_compliant:
        compliance_scores.append(100)  # Sector is OK
    else:
        compliance_scores.append(0)

    # Check debt-to-equity
    de_ratio, de_status = check_debt_to_equity(symbol)
    
    # Try fetching FMP raw balance sheet metrics
    # If successful, use them to overwrite inaccurate Finnhub DE where possible
    fmp_metrics = None
    try:
        fmp_metrics = get_halal_metrics_fmp(symbol)
    except Exception:
        pass
        
    if de_ratio is not None:
        if de_ratio < 1.5:
            compliance_scores.append(80)
        else:
            compliance_scores.append(40)
            issues.append(f"High debt-to-equity ratio: {de_ratio:.2f}")

    # Check FMP specific Interest Income non-permissible rule (<5%)
    if fmp_metrics and fmp_metrics.get("total_revenue", 0) > 0:
        int_revenue = fmp_metrics.get("interest_income", 0)
        total_revenue = fmp_metrics.get("total_revenue", 0)
        impermissible_income_ratio = int_revenue / total_revenue
        if impermissible_income_ratio > 0.05:
            compliance_scores.append(0)
            issues.append(f"Impermissible income ({impermissible_income_ratio*100:.1f}%) exceeds 5% limit.")

    # Calculate overall compliance score
    overall_score = sum(compliance_scores) / len(compliance_scores) if compliance_scores else 0

    is_halal = overall_score >= 70  # 70% compliance threshold

    return {
        'symbol': symbol,
        'company_name': info.get('company_name', symbol),
        'sector': sector,
        'is_halal': is_halal,
        'compliance_score': overall_score,
        'debt_to_equity': de_ratio,
        'de_status': de_status,
        'issues': issues,
        'details': info,
        'methodologies': evaluate_methodologies(de_ratio, sector_compliant, fmp_metrics)
    }


def get_halal_stocks_list() -> List[str]:
    """Get pre-screened halal stocks"""
    return HALAL_STOCKS
