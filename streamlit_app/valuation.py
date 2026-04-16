import math
from typing import Dict, List
import streamlit as st
from finnhub_client import get_fundamental_ratios, get_company_news, get_quote
import datetime

def calculate_graham_number(eps: float, bvps: float) -> float:
    """
    Calculates the Benjamin Graham Number for intrinsic value.
    Formula: sqrt(22.5 * EPS * BVPS)
    """
    if eps is None or bvps is None or eps < 0 or bvps < 0:
        return 0.0
    return math.sqrt(22.5 * eps * bvps)

def render_valuation_metrics(symbol: str, current_price: float):
    metrics = get_fundamental_ratios(symbol).get('metric', {})
    
    eps = metrics.get('epsTTM', 0)
    bvps = metrics.get('bookValuePerShareAnnual', 0)
    pe_ratio = metrics.get('peTrailingTTM', 0)
    pb_ratio = metrics.get('pbAnnual', 0)
    
    graham_number = calculate_graham_number(eps, bvps)
    
    st.subheader("⚖️ Valuation & Intrinsic Value Estimate")
    st.markdown("For the sensible long-term investor, it is critical not just to buy a good business, but to buy it at a **fair price**. The Benjamin Graham Number helps identify the 'maximum fair value'.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Graham Number (Max Fair Value)", f"${graham_number:.2f}" if graham_number > 0 else "N/A")
    with col2:
        st.metric("EPS (TTM)", f"${eps:.2f}" if eps else "N/A")
    with col3:
        st.metric("Book Value / Share", f"${bvps:.2f}" if bvps else "N/A")
    with col4:
        st.metric("P/E Ratio", f"{pe_ratio:.2f}x" if pe_ratio else "N/A")
        
    if current_price and graham_number > 0:
        discount = ((graham_number - current_price) / current_price) * 100
        if current_price < graham_number:
            st.success(f"✅ **Undervalued:** Trading at a {discount:.1f}% discount to its Graham Number.")
        else:
            premium = abs(discount)
            st.warning(f"⚠️ **Premium Valuation:** Trading at a {premium:.1f}% premium above its Graham Number. (Tech stocks typically trade at a premium).")
    elif graham_number == 0:
        st.error("❌ **Cannot Calculate Graham Number:** Company has negative earnings (EPS) or negative Book Value.")

def render_company_news(symbol: str):
    st.subheader("📰 Recent Company News")
    st.markdown(f"Latest headlines for **{symbol}** driving the market sentiment.")
    
    news = get_company_news(symbol, limit=4)
    if not news:
        st.info("No recent news found from Finnhub.")
        return
        
    for item in news:
        date_str = datetime.datetime.fromtimestamp(item.get('datetime', 0)).strftime('%Y-%m-%d %H:%M')
        headline = item.get('headline', 'No Headline')
        source = item.get('source', 'Unknown')
        url = item.get('url', '#')
        summary = item.get('summary', '')
        
        with st.expander(f"**{source}**: {headline} ({date_str})"):
            st.write(summary)
            st.markdown(f"[Read full article]({url})")

