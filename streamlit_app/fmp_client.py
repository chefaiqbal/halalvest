import requests
import streamlit as st
import os
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Get FMP API key
try:
    FMP_API_KEY = st.secrets.get("FMP_API_KEY", os.getenv("FMP_API_KEY", ""))
except Exception:
    FMP_API_KEY = os.getenv("FMP_API_KEY", "")

FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"

@st.cache_data(ttl=3600, show_spinner=False)
def get_halal_metrics_fmp(symbol: str) -> Optional[Dict]:
    """
    Fetches raw financial metrics for Halal compliance testing:
    Total Debt, Total Assets, Market Cap
    """
    if not FMP_API_KEY:
        logger.warning("No FMP API Key found. Returning None.")
        return None

    symbol = symbol.strip().upper()
    try:
        # 1. Get Balance Sheet for Assets and Debt
        bs_url = f"{FMP_BASE_URL}/balance-sheet-statement/{symbol}?limit=1&apikey={FMP_API_KEY}"
        bs_res = requests.get(bs_url, timeout=10)
        bs_res.raise_for_status()
        bs_data = bs_res.json()

        if not bs_data or not isinstance(bs_data, list):
            return None
            
        latest_bs = bs_data[0]
        total_assets = latest_bs.get('totalAssets', 0)
        total_debt = latest_bs.get('totalDebt', 0)
        
        # 2. Get Income Statement for Interest Income
        is_url = f"{FMP_BASE_URL}/income-statement/{symbol}?limit=1&apikey={FMP_API_KEY}"
        is_res = requests.get(is_url, timeout=10)
        is_data = is_res.json() if is_res.status_code == 200 else []
        
        interest_income = 0
        total_revenue = 0
        if is_data and isinstance(is_data, list):
            interest_income = is_data[0].get('interestIncome', 0)
            total_revenue = is_data[0].get('revenue', 0)

        # 3. Get Quote for Market Cap
        quote_url = f"{FMP_BASE_URL}/quote/{symbol}?apikey={FMP_API_KEY}"
        quote_res = requests.get(quote_url, timeout=10)
        quote_res.raise_for_status()
        quote_data = quote_res.json()

        if not quote_data or not isinstance(quote_data, list):
            return None

        market_cap = quote_data[0].get('marketCap', 0)

        return {
            "total_assets": total_assets,
            "total_debt": total_debt,
            "market_cap": market_cap,
            "interest_income": interest_income,
            "total_revenue": total_revenue
        }
    except Exception as e:
        logger.error(f"FMP metrics error for {symbol}: {e}")
        return None
