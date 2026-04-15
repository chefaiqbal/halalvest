import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from halal_screening import get_halal_stocks_list, screen_stock_halal
from recommendation_engine import get_recommendation
import yfinance as yf

# Page config
st.set_page_config(
    page_title="HalalVest - Halal Stock Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []


def add_to_watchlist(symbol):
    """Add stock to watchlist"""
    if symbol not in st.session_state.watchlist:
        st.session_state.watchlist.append(symbol)
        st.success(f"✅ {symbol} added to watchlist!")
    else:
        st.warning(f"⚠️ {symbol} is already in your watchlist")


def remove_from_watchlist(symbol):
    """Remove stock from watchlist"""
    if symbol in st.session_state.watchlist:
        st.session_state.watchlist.remove(symbol)
        st.success(f"✅ {symbol} removed from watchlist!")


# Title and description
st.title("📈 HalalVest - Halal Stock Tracker & Analyzer")
st.markdown("""
Track halal-screened stocks, get AI-powered buy/sell/hold recommendations, and make sound investment decisions.
**Disclaimer:** This tool is for educational purposes only. Always do your own research and consult with a financial advisor.
""")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page:",
    ["Dashboard", "Stock Analysis", "Halal Screening", "My Watchlist", "About"])

# ==================== DASHBOARD PAGE ====================
if page == "Dashboard":
    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Halal Stocks Available", len(get_halal_stocks_list()))
    with col2:
        st.metric("Your Watchlist", len(st.session_state.watchlist))
    with col3:
        st.metric("Last Updated", "Real-time")

    st.subheader("Quick Stock Overview - Top Halal Stocks")

    # Show top 10 halal stocks with quick analysis
    halal_stocks = get_halal_stocks_list()[:15]

    stock_data = []
    for symbol in halal_stocks:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = yf.download(symbol, period='1d', progress=False)

            if not hist.empty:
                price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else price
                change = ((price - prev_price) / prev_price * 100) if prev_price > 0 else 0

                stock_data.append({
                    'Symbol': symbol,
                    'Price': f"${price:.2f}",
                    'Change %': f"{change:+.2f}%",
                    'Company': info.get('longName', symbol),
                })
        except:
            pass

    if stock_data:
        df = pd.DataFrame(stock_data)
        st.dataframe(df, use_container_width=True)


# ==================== STOCK ANALYSIS PAGE ====================
elif page == "Stock Analysis":
    st.header("🔍 Stock Analysis")

    col1, col2 = st.columns([3, 1])
    with col1:
        stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, MSFT, JNJ):", "MSFT").upper()
    with col2:
        if st.button("🔎 Analyze"):
            st.session_state.analyze_symbol = stock_symbol

    if 'analyze_symbol' in st.session_state:
        symbol = st.session_state.analyze_symbol

        with st.spinner(f"Analyzing {symbol}..."):
            # Get recommendation
            rec = get_recommendation(symbol)

            if 'error' in rec:
                st.error(f"❌ Error: {rec['error']}")
            else:
                # Halal screening
                halal = screen_stock_halal(symbol)

                # Recommendation card
                st.subheader(f"📌 {symbol} - {halal['company_name']}")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Recommendation", rec['recommendation'],
                             f"Score: {rec['combined_score']:.1f}/100")
                with col2:
                    st.metric("Confidence", f"{rec['confidence']:.1f}%")
                with col3:
                    st.metric("Halal Score", f"{halal['compliance_score']:.0f}%",
                             "✅ Compliant" if halal['is_halal'] else "❌ Review needed")
                with col4:
                    if st.button("⭐ Add to Watchlist", key=f"add_{symbol}"):
                        add_to_watchlist(symbol)

                st.markdown("---")

                # Analysis breakdown
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("📊 Technical Analysis")
                    tech = rec['technical_analysis']
                    st.write(f"**Current Price:** ${tech['current_price']:.2f}")
                    st.write(f"**Change:** {tech['price_change_pct']:+.2f}%")
                    st.write(f"**Trend:** {tech['trend']}")
                    st.write(f"**RSI (14):** {tech['rsi']:.2f}" if tech.get('rsi') else "RSI: N/A")
                    st.write(f"**Volume Trend:** {tech['volume']['trend']}")
                    st.write(f"**Technical Score:** {rec['technical_score']:.0f}/100")

                with col2:
                    st.subheader("💼 Fundamental Analysis")
                    fund = rec['fundamental_analysis']
                    st.write(f"**P/E Ratio:** {fund['pe_interpretation']}")
                    st.write(f"**Debt-to-Equity:** {fund['de_interpretation']}")
                    st.write(f"**ROE:** {fund['roe_interpretation']}")
                    st.write(f"**Profit Margin:** {fund['pm_interpretation']}")
                    st.write(f"**Fundamental Score:** {rec['fundamental_score']:.0f}/100")

                st.markdown("---")

                # Halal screening details
                st.subheader("✅ Halal Compliance")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Sector:** {halal['sector']}")
                with col2:
                    st.write(f"**Compliance Score:** {halal['compliance_score']:.0f}%")
                with col3:
                    st.write(f"**D/E Ratio:** {halal['de_status']}")

                if halal['issues']:
                    st.warning("**⚠️ Issues Found:**")
                    for issue in halal['issues']:
                        st.write(f"• {issue}")

                st.markdown("---")
                st.info(f"**Recommendation:** {rec['explanation']}")


# ==================== HALAL SCREENING PAGE ====================
elif page == "Halal Screening":
    st.header("✅ Halal Stock Screening")

    st.markdown("""
    This page shows stocks that comply with Islamic finance principles:
    - ✅ No prohibited sectors (alcohol, tobacco, gambling, etc.)
    - ✅ Reasonable debt-to-equity ratios (avoiding riba)
    - ✅ Operational efficiency and profitability
    """)

    halal_stocks = get_halal_stocks_list()
    st.write(f"**Available Halal-Screened Stocks: {len(halal_stocks)}**")

    # Display stocks in columns
    cols = st.columns(5)
    for idx, symbol in enumerate(halal_stocks):
        with cols[idx % 5]:
            if st.button(symbol, key=f"screen_{symbol}"):
                st.session_state.selected_symbol = symbol

    if 'selected_symbol' in st.session_state:
        symbol = st.session_state.selected_symbol
        halal = screen_stock_halal(symbol)

        st.subheader(f"Screening Results: {symbol}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Compliance Score", f"{halal['compliance_score']:.0f}%")
        with col2:
            st.metric("Status", "✅ Halal" if halal['is_halal'] else "❌ Review")
        with col3:
            st.metric("D/E Ratio", f"{halal['debt_to_equity']:.2f}" if halal['debt_to_equity'] else "N/A")

        if halal['issues']:
            st.warning("Issues:")
            for issue in halal['issues']:
                st.write(f"• {issue}")
        else:
            st.success("No compliance issues found! ✅")


# ==================== WATCHLIST PAGE ====================
elif page == "My Watchlist":
    st.header("⭐ My Watchlist")

    if len(st.session_state.watchlist) == 0:
        st.info("Your watchlist is empty. Add stocks from the Stock Analysis page!")
    else:
        st.write(f"**{len(st.session_state.watchlist)} stocks in your watchlist**")

        for symbol in st.session_state.watchlist:
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    price = info.get('currentPrice', 'N/A')

                    rec = get_recommendation(symbol)
                    if 'error' not in rec:
                        st.write(f"**{symbol}** - {rec['recommendation']}")
                        st.caption(f"Score: {rec['combined_score']:.0f}/100 | Confidence: {rec['confidence']:.0f}%")
                    else:
                        st.write(f"**{symbol}**")
                except:
                    st.write(f"**{symbol}**")

            with col2:
                if st.button("📊 View", key=f"view_{symbol}"):
                    st.session_state.analyze_symbol = symbol
                    st.rerun()

            with col3:
                if st.button("❌ Remove", key=f"remove_{symbol}"):
                    remove_from_watchlist(symbol)
                    st.rerun()


# ==================== ABOUT PAGE ====================
elif page == "About":
    st.header("About HalalVest")

    st.markdown("""
    ## What is HalalVest?

    HalalVest is a free, open-source stock tracking and analysis tool designed for Islamic investing.

    ### Features:
    - **Halal Stock Screening**: Automatically filters stocks by Islamic finance principles
    - **Technical Analysis**: SMA, RSI, MACD, Volume trends
    - **Fundamental Analysis**: P/E ratios, earnings, ROE, profit margins
    - **Buy/Sell/Hold Recommendations**: Combined technical and fundamental scoring
    - **Mobile-Friendly**: Works great on iOS Safari

    ### How It Works:
    1. **Technical Analysis (50%)**: Identifies market trends and momentum
    2. **Fundamental Analysis (50%)**: Assesses company health and profitability
    3. **Combined Score**: Generates buy/sell/hold recommendations with confidence levels

    ### Important Disclaimer:
    ⚠️ **This tool is for educational purposes only!**
    - Not financial advice
    - Always do your own research
    - Consult with a financial advisor
    - Never invest based solely on this tool
    - Past performance doesn't guarantee future results

    ### Data Sources:
    - Stock data: Yahoo Finance
    - Company information: Yahoo Finance API

    ### Technology:
    - Backend: Python
    - Frontend: Streamlit
    - Hosting: Streamlit Cloud (Free)
    """)


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px;">
    HalalVest © 2024 | Built with ❤️ for the Islamic investing community<br>
    <b>Disclaimer:</b> For educational purposes only. Not financial advice.
</div>
""", unsafe_allow_html=True)

